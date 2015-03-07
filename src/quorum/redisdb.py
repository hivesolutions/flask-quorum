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

import os
import json
import shelve

from . import config
from . import exceptions

try: import redis
except: redis = None

connection = None
""" The global connection object that should persist
the connection relation with the database service """

url = None
""" The global variable containing the url to be used
for the connection with the service """

class RedisMemory(object):
    """
    "Local" in memory stub object that simulates
    the redis interface, useful for debugging.

    This memory interface may create problems in
    a multiple process environment (non shared memory).
    """

    values = None
    """ The map containing the various values to
    be set in the memory map, simulates the redis
    data store """

    def __init__(self):
        self.values = {}

    def get(self, name):
        name_s = str(name)
        return self.values.get(name_s)

    def set(self, name, value):
        name_s = str(name)
        self.values[name_s] = value

    def setex(self, name, value, expire):
        self.set(name, value)

    def delete(self, name):
        if not name in self.values: return
        del self.values[name]

class RedisShelve(RedisMemory):
    """
    "Local" in persistent stub object that simulates
    the redis interface, useful for debugging.

    This shelve interface requires a writable path
    where its persistent file may be written.
    """

    def __init__(self, path = "redis.shelve"):
        RedisMemory.__init__(self)
        base_path = config.conf("SESSION_FILE_PATH", "")
        file_path = os.path.join(base_path, path)
        self.values = shelve.open(
            file_path,
            protocol = 2,
            writeback = True
        )

    def close(self):
        self.values.close()

    def set(self, name, value):
        RedisMemory.set(self, name, value)
        self.values.sync()

    def delete(self, name):
        name_s = str(name)
        if not name_s in self.values: return
        del self.values[name_s]

def get_connection():
    return _get_connection(url)

def dumps(*args):
    return json.dumps(*args)

def _get_connection(url):
    global connection
    if redis == None: raise exceptions.ModuleNotFound("redis")
    if not connection: connection = url and redis.from_url(url) or RedisShelve()
    return connection
