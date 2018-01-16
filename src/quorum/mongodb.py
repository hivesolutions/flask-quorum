#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
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
except: pymongo = None

try: import bson.json_util
except: bson = None

connection = None
""" The global connection object that should persist
the connection relation with the database service """

url = "mongodb://localhost"
""" The global variable containing the URL to be used
for the connection with the service """

database = "master"
""" The global variable containing the value for the
database to be used in the connection with the service """

class MongoMap(object):
    """
    Encapsulates a mongo collection to provide an interface
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

def reset_connection():
    return _reset_connection()

def get_db():
    connection = get_connection()
    result = _pymongo().uri_parser.parse_uri(url)
    _database = result.get("database", None) or database
    db = connection[_database]
    return db

def drop_db():
    db = get_db()
    names = db.collection_names()
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

def is_new():
    return int(_pymongo().version[0]) >= 3 if pymongo else False

def _store_find_and_modify(store, *args, **kwargs):
    if is_new(): store.find_one_and_update(*args, **kwargs)
    else: store.find_and_modify(*args, **kwargs)

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

def _reset_connection():
    global connection
    if not connection: return
    if is_new(): connection.close()
    else: connection.disconnect()
    connection = None

def _pymongo(verify = True):
    if verify: util.verify(
        not pymongo == None,
        message = "pymongo library not available",
        exception = exceptions.OperationalError
    )
    return pymongo
