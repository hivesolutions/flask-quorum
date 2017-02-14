#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
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

from . import log
from . import legacy
from . import config
from . import mongodb
from . import exceptions

class DataAdapter(object):

    def __init__(self, *args, **kwargs):
        self._inc = 0
        self._machine_bytes = self.__machine_bytes()
        self._inc_lock = threading.RLock()

    @classmethod
    def name_g(cls):
        return cls.__name__[:-7].lower()

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

    @property
    def name(self):
        cls = self.__class__
        return cls.name_g()

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
        return MongoCollection(self, name, collection)

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
        self.storage = config.conf("TINY_STORAGE", "json")
        self.file_path = kwargs.get("file_path", self.file_path)
        self._db = None

    def collection(self, name, *args, **kwargs):
        db = self.get_db()
        table = db.table(name)
        return TinyCollection(self, name, table)

    def get_db(self):
        if not self._db == None: return self._db
        method = getattr(self, "_get_db_%s" % self.storage)
        self._db = method()
        return self._db

    def drop_db(self, *args, **kwargs):
        if self._db == None: return
        db = self.get_db()
        db.purge_tables()
        db.close()
        self._db = None
        method = getattr(self, "_drop_db_%s" % self.storage)
        method()

    def _get_db_json(self):
        import tinydb
        return tinydb.TinyDB(self.file_path)

    def _get_db_memory(self):
        import tinydb
        return tinydb.TinyDB(
            storage = tinydb.storages.MemoryStorage
        )

    def _drop_db_json(self):
        os.remove(self.file_path)

    def _drop_db_memory(self):
        pass

class Collection(object):

    def __init__(self, owner, name):
        self.owner = owner
        self.name = name

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

    def log(self, operation, *args, **kwargs):
        show_queries = config.conf("SHOW_QUERIES", False, cast = bool)
        if not show_queries: return
        extra = kwargs or args
        log.debug(
            "[%s] %10s -> %12s <-> %s" %\
            (self.owner.name, operation, self.name, str(extra)[:2046])
        )

    def _id(self, *args, **kwargs):
        return self.owner._id(*args, **kwargs)

class MongoCollection(Collection):

    def __init__(self, owner, name, base):
        Collection.__init__(self, owner, name)
        self._base = base

    def find(self, *args, **kwargs):
        self.log("find", *args, **kwargs)
        return self._base.find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        self.log("find_one", *args, **kwargs)
        return self._base.find_one(*args, **kwargs)

    def find_and_modify(self, *args, **kwargs):
        self.log("find_and_modify", *args, **kwargs)
        return mongodb._store_find_and_modify(self._base, *args, **kwargs)

    def insert(self, *args, **kwargs):
        self.log("insert", *args, **kwargs)
        return mongodb._store_insert(self._base, *args, **kwargs)

    def update(self, *args, **kwargs):
        self.log("update", *args, **kwargs)
        return mongodb._store_update(self._base, *args, **kwargs)

    def remove(self, *args, **kwargs):
        self.log("remove", *args, **kwargs)
        return mongodb._store_remove(self._base, *args, **kwargs)

    def count(self, *args, **kwargs):
        self.log("count", *args, **kwargs)
        return self._base.count(*args, **kwargs)

    def ensure_index(self, *args, **kwargs):
        self.log("ensure_index", *args, **kwargs)
        simple = kwargs.pop("simple", False)
        if simple: return mongodb._store_ensure_index(self._base, *args, **kwargs)
        else: return mongodb._store_ensure_index_all(self._base, *args, **kwargs)

class TinyCollection(Collection):

    def __init__(self, owner, name, base):
        Collection.__init__(self, owner, name)
        self._base = base

    def find(self, *args, **kwargs):
        self.log("find", *args, **kwargs)
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        results = self._base.search(condition)
        return self._to_results(results, kwargs)

    def find_one(self, *args, **kwargs):
        self.log("find_one", *args, **kwargs)
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        results = self._base.search(condition)
        results = self._to_results(results, kwargs)
        return results[0] if results else None

    def find_and_modify(self, *args, **kwargs):
        self.log("find_and_modify", *args, **kwargs)
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
        if found: self.update(filter, {"$set" : object})
        else: self.insert(object)
        return dict(object)

    def insert(self, *args, **kwargs):
        self.log("insert", *args, **kwargs)
        object = args[0] if len(args) > 0 else dict()
        has_id = "_id" in object
        if not has_id: object["_id"] = self._id()
        self._base.insert(object)
        return object

    def update(self, *args, **kwargs):
        self.log("update", *args, **kwargs)
        filter = args[0] if len(args) > 0 else dict()
        updater = args[1] if len(args) > 1 else dict()
        condition = self._to_condition(filter)
        object = updater.get("$set", dict())
        return self._base.update(object, condition)

    def remove(self, *args, **kwargs):
        self.log("remove", *args, **kwargs)
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        return self._base.remove(condition)

    def count(self, *args, **kwargs):
        self.log("count", *args, **kwargs)
        filter = args[0] if len(args) > 0 else dict()
        condition = self._to_condition(filter)
        return self._base.count(condition)

    def ensure_index(self, *args, **kwargs):
        self.log("ensure_index", *args, **kwargs)

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

    def _to_results(self, results, kwargs, build = True):
        sort = kwargs.get("sort", [])
        skip = kwargs.get("skip", 0)
        limit = kwargs.get("limit", None)

        limit = None if limit == 0 else limit
        reverse = sort[0][1] == -1 if sort else False

        def sorter(value):
            result = []
            for item in sort: result.append(value[item[0]])
            return tuple(result)

        if sort: results.sort(key = sorter, reverse = reverse)
        if skip or limit: results = results[slice(skip, skip + limit, 1)]
        if build: results = [dict(result) for result in results]
        return results

    def _to_update(self, modification, object = None):
        object = object or dict()
        increments = modification.get("$inc", {})
        for name, increment in legacy.iteritems(increments):
            value = object.get(name, 0)
            value += increment
            object[name] = value
        return object
