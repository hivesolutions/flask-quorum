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

from . import exceptions

try: import boto
except: boto = None

connection = None
""" The global wide connection to the amazon server
that is meant to be used across sessions """

bucket = None
""" The global bucket reference to be used to create
new key values and to retrieve existing ones, only one
bucket exists for a given quorum diffusion scope """

id = None
""" The id of the client that is going to be used in the
connections to be established to the amazon servers """

secret = None
""" The secret of the client that is going to be used in the
connections to be established to the amazon servers """

bucket_name = None
""" The name of the bucket to be used to create and retrieve
keys from the amazon services """

def get_connection():
    global connection
    if boto == None: raise exceptions.ModuleNotFound("boto")
    if connection: return connection
    connection = boto.connect_s3(id, secret)
    return connection

def get_bucket():
    global bucket
    connection = get_connection()
    if bucket: return bucket
    bucket = connection.get_bucket(bucket_name)
    return bucket

def clear_bucket():
    bucket = get_bucket()
    keys = bucket.get_all_keys()
    for key in keys: key.delete()

def get_key(name):
    bucket = get_bucket()
    key = boto.s3.key.Key(bucket)
    key.key = name
    return key

def exists_key(name):
    bucket = get_bucket()
    key = boto.s3.key.Key(bucket)
    key.key = name
    return key.exists()

def delete_key(name):
    bucket = get_bucket()
    bucket.delete_key(name)
