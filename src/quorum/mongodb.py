#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2021 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2021 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json

from . import util
from . import legacy
from . import common
from . import typesf
from . import exceptions

try: import pymongo
except ImportError: pymongo = None

try: import bson.json_util
except ImportError: bson = None

try: import motor.motor_asyncio
except ImportError: motor = None

connection = None
""" The global connection object that should persist
the connection relation with the database service """

connection_a = None
""" The global connection reference for the async version
of the Mongo client """

url = "mongodb://localhost"
""" The global variable containing the URL to be used
for the connection with the service """

database = "master"
""" The global variable containing the value for the
database to be used in the connection with the service """

class MongoMap(object):
    """
    Encapsulates a MongoDB collection to provide an interface
    that is compatible with the "normal" key value access
    offered by the python dictionary (map).
    """

    collection = None
    """ The collection to be used as the underlying structure
    for the data access """

    key = None
    """ The name of the key to be used for the "default" search
    for value providing """

    def __init__(self, collection, key = "id"):
        self.collection = collection
        self.key = key

    def get(self, value, default = None):
        return self.collection.find_one({self.key : value}) or default

class MongoEncoder(json.JSONEncoder):

    def default(self, obj, **kwargs):
        if not bson: return json.JSONEncoder.default(self, obj, **kwargs)
        if isinstance(obj, bson.objectid.ObjectId): return str(obj)
        if isinstance(obj, legacy.BYTES): return legacy.str(obj, encoding = "utf-8")
        else: return json.JSONEncoder.default(self, obj, **kwargs)

def get_connection():
    return _get_connection(url)

def get_connection_a():
    return _get_connection_a(url)

def reset_connection():
    return _reset_connection()

def reset_connection_a():
    return _reset_connection_a()

def get_db():
    connection = get_connection()
    result = _pymongo().uri_parser.parse_uri(url)
    _database = result.get("database", None) or database
    db = connection[_database]
    return db

def get_db_a():
    connection = get_connection_a()
    result = _pymongo().uri_parser.parse_uri(url)
    _database = result.get("database", None) or database
    db = connection[_database]
    return db

def drop_db():
    db = get_db()
    names = _list_names(db)
    for name in names:
        if name.startswith("system."): continue
        db.drop_collection(name)

def drop_db_a():
    db = get_db_a()
    names = _list_names(db)
    for name in names:
        if name.startswith("system."): continue
        db.drop_collection(name)

def object_id(value):
    return bson.ObjectId(value)

def dumps(*args):
    return json.dumps(default = serialize, *args)

def serialize(obj):
    if isinstance(obj, common.model().Model): return obj.model
    if isinstance(obj, typesf.AbstractType): return obj.json_v()
    return bson.json_util.default(obj)

def directions(all = False):
    return (
        _pymongo().ASCENDING,
        _pymongo().DESCENDING,
        _pymongo().HASHED
    ) if all else (
        _pymongo().ASCENDING,
        _pymongo().DESCENDING
    )

def is_mongo(obj):
    if bson and isinstance(obj, bson.ObjectId): return True
    if bson and isinstance(obj, bson.DBRef): return True
    return False

def is_new(major = 3, minor = 0, patch = 0):
    _major, _minor, _patch = _version_t()
    if _major > major: return True
    elif _major < major: return False
    if _minor > minor: return True
    elif _minor < minor: return False
    if _patch >= patch: return True
    else: return False

def _list_names(db, *args, **kwargs):
    if is_new(3, 7): return db.list_collection_names()
    else: return db.collection_names()

def _count(store, *args, **kwargs):
    if len(args) == 0: args = [{}]
    if is_new(3, 7): return store.count_documents(*args, **kwargs)
    return store.count(*args, **kwargs)

def _count_documents(store, *args, **kwargs):
    if len(args) == 0: args = [{}]
    if is_new(3, 7): return store.count_documents(*args, **kwargs)
    result = store.find(*args, **kwargs)
    return result.count()

def _store_find_and_modify(store, *args, **kwargs):
    if is_new(): return store.find_one_and_update(*args, **kwargs)
    else: return store.find_and_modify(*args, **kwargs)

def _store_insert(store, *args, **kwargs):
    if is_new(): store.insert_one(*args, **kwargs)
    else: store.insert(*args, **kwargs)

def _store_update(store, *args, **kwargs):
    if is_new(): store.update_one(*args, **kwargs)
    else: store.update(*args, **kwargs)

def _store_remove(store, *args, **kwargs):
    if is_new(): store.delete_many(*args, **kwargs)
    else: store.remove(*args, **kwargs)

def _store_ensure_index(store, *args, **kwargs):
    kwargs["background"] = kwargs.get("background", True)
    if is_new(): store.create_index(*args, **kwargs)
    else: store.ensure_index(*args, **kwargs)

def _store_ensure_index_many(store, *args, **kwargs):
    directions_l = kwargs.pop("directions", None)
    if directions_l == "all": directions_l = directions(all = True)
    elif directions_l == None: directions_l = directions()
    for direction in directions_l:
        _args = list(args)
        _args[0] = [(_args[0], direction)]
        _store_ensure_index(store, *_args, **kwargs)

def _get_connection(url, connect = False):
    global connection
    if pymongo == None: raise exceptions.ModuleNotFound("pymongo")
    if connection: return connection
    if is_new(): connection = _pymongo().MongoClient(url, connect = connect)
    else: connection = _pymongo().Connection(url)
    return connection

def _get_connection_a(url, connect = False):
    global connection_a
    if motor == None: raise exceptions.ModuleNotFound("motor")
    if connection_a: return connection_a
    connection_a = _motor().AsyncIOMotorClient(url, connect = connect)
    return connection_a

def _reset_connection():
    global connection
    if not connection: return
    if is_new(): connection.close()
    else: connection.disconnect()
    connection = None

def _reset_connection_a():
    global connection_a
    if not connection_a: return
    connection_a.close()
    connection = None

def _version_t():
    pymongo_l = _pymongo()
    if hasattr(pymongo_l, "_version_t"): return pymongo_l._version_t
    version_l = pymongo.version.split(".", 2)
    if len(version_l) == 2: version_l.append("0")
    major_s, minor_s, patch_s = version_l
    pymongo_l._version_t = (int(major_s), int(minor_s), int(patch_s))
    return pymongo_l._version_t

def _pymongo(verify = True):
    if verify: util.verify(
        not pymongo == None,
        message = "PyMongo library not available",
        exception = exceptions.OperationalError
    )
    return pymongo

def _motor(verify = True):
    if verify: util.verify(
        not motor == None,
        message = "Motor library not available",
        exception = exceptions.OperationalError
    )
    return motor.motor_asyncio
