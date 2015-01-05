#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json

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

url = "mongodb://localhost:27017"
""" The global variable containing the url to be used
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

def get_connection():
    return _get_connection(url)

def get_db():
    connection = get_connection()
    result = pymongo.uri_parser.parse_uri(url)
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
    if isinstance(obj, typesf.Type): return obj.json_v()
    return bson.json_util.default(obj)

def is_mongo(obj):
    if bson and isinstance(obj, bson.ObjectId): return True
    if bson and isinstance(obj, bson.DBRef): return True
    return False

def _get_connection(url):
    global connection
    if pymongo == None: raise exceptions.ModuleNotFound("pymongo")
    if not connection: connection = pymongo.Connection(url)
    return connection
