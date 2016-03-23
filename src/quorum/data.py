#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Flask Quorum.
#
# Hive Flask Quorum is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Flask Quorum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Flask Quorum. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import time
import struct
import socket
import hashlib
import binascii
import threading

from . import legacy
from . import config
from . import mongodb
from . import exceptions

class DataAdapter(object):

    def __init__(self, *args, **kwargs):
        self._inc = 0
        self._machine_bytes = self.__machine_bytes()
        self._inc_lock = threading.RLock()

    def collection(self, name, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def get_db(self):
        raise exceptions.NotImplementedError()

    def drop_db(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def object_id(self, value = None):
        if not value: return self._id()
        if not len(value) == 24:
            raise exceptions.OperationalError(
                "Expected object id of length 24 chars"
            )
        return value

    def _id(self):
        token = struct.pack(">i", int(time.time()))
        token += self._machine_bytes
        token += struct.pack(">H", os.getpid() % 0xffff)
        self._inc_lock.acquire()
        try:
            token += struct.pack(">i", self._inc)[1:4]
            self._inc = (self._inc + 1) % 0xffffff
        except:
            self._inc_lock.release()
        token_s = binascii.hexlify(token)
        token_s = legacy.str(token_s)
        return token_s

    def __machine_bytes(self):
        machine_hash = hashlib.md5()
        hostname = socket.gethostname()
        hostname = legacy.bytes(hostname)
        machine_hash.update(hostname)
        return machine_hash.digest()[0:3]

class MongoAdapter(DataAdapter):

    def collection(self, name, *args, **kwargs):
        db = self.get_db()
        collection = db[name]
        return MongoCollection(self, collection)

    def get_db(self):
        return mongodb.get_db()

    def drop_db(self, *args, **kwargs):
        return mongodb.drop_db()

    def object_id(self, value = None):
        if not value: return self._id()
        return mongodb.object_id(value)

    def _id(self):
        return mongodb.object_id(None)

class TinyAdapter(DataAdapter):

    def __init__(self, *args, **kwargs):
        DataAdapter.__init__(self, *args, **kwargs)
        self.file_path = config.conf("TINY_PATH", "db.json")
        self.file_path = kwargs.get("file_path", self.file_path)
        self._db = None

    def collection(self, name, *args, **kwargs):
        db = self.get_db()
        table = db.table(name)
        return TinyCollection(self, table)

    def get_db(self):
        import tinydb
        if self._db: return self._db
        self._db = tinydb.TinyDB(self.file_path)
        return self._db

    def drop_db(self, *args, **kwargs):
        db = self.get_db()
        db.purge_tables()
        db.close()
        self._db = None
        os.remove(self.file_path)

class Collection(object):

    def __init__(self, owner):
        self.owner = owner

    def find(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def find_one(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def find_and_modify(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def insert(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def update(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def remove(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def count(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def ensure_index(self, *args, **kwargs):
        raise exceptions.NotImplementedError()

    def object_id(self, *args, **kwargs):
        return self.owner.object_id(*args, **kwargs)

    def _id(self, *args, **kwargs):
        return self.owner._id(*args, **kwargs)

class MongoCollection(Collection):

    def __init__(self, owner, base):
        Collection.__init__(self, owner)
        self._base = base

    def find(self, *args, **kwargs):
        return self._base.find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        return self._base.find_one(*args, **kwargs)

    def find_and_modify(self, *args, **kwargs):
        return mongodb._store_find_and_modify(self._base, *args, **kwargs)

    def insert(self, *args, **kwargs):
        return mongodb._store_insert(self._base, *args, **kwargs)

    def update(self, *args, **kwargs):
        return mongodb._store_update(self._base, *args, **kwargs)

    def remove(self, *args, **kwargs):
        return mongodb._store_remove(self._base, *args, **kwargs)

    def count(self, *args, **kwargs):
        return self._base.count(*args, **kwargs)

    def ensure_index(self, *args, **kwargs):
        return mongodb._store_ensure_index(self._base, *args, **kwargs)

class TinyCollection(Collection):

    def __init__(self, owner, base):
        Collection.__init__(self, owner)
        self._base = base

    def find(self, *args, **kwargs):
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        return self._base.search(condition)

    def find_one(self, *args, **kwargs):
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        return self._base.get(condition)

    def find_and_modify(self, *args, **kwargs):
        filter = args[0] if len(args) > 0 else dict()
        modification = args[1] if len(args) > 1 else dict()
        create = kwargs.get("new", False)
        condition = self._to_condition(filter)
        object = self._base.get(condition)
        found = True if object else False
        if not found and not create:
            raise exceptions.OperationalError("No object found")
        if not found: object = dict(filter)
        object = self._to_update(modification, object = object)
        if found: self.update(object)
        else: self.insert(object)
        return object

    def insert(self, *args, **kwargs):
        object = args[0] if len(args) > 0 else dict()
        has_id = "_id" in object
        if not has_id: object["_id"] = self._id()
        self._base.insert(object)
        return object

    def update(self, *args, **kwargs):
        filter = args[0] if len(args) > 0 else dict()
        updater = args[1] if len(args) > 1 else dict()
        condition = self._to_condition(filter)
        object = updater.get("$set", dict())
        return self._base.update(object, condition)

    def remove(self, *args, **kwargs):
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        return self._base.remove(condition)

    def count(self, *args, **kwargs):
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        return self._base.count(condition)

    def ensure_index(self, *args, **kwargs):
        pass

    def _to_condition(self, filter):
        import tinydb
        query = tinydb.Query()
        condition = query._id.exists()
        for name, value in legacy.iteritems(filter):
            if name.startswith("$"): continue
            query = tinydb.Query()
            _condition = getattr(query, name).__eq__(value)
            condition &= _condition
        return condition

    def _to_update(self, modification, object = None):
        object = object or dict()
        increments = modification.get("$inc", {})
        for name, increment in legacy.iteritems(increments):
            value = object.get(name, 0)
            value += increment
            object[name] = value
        return object
