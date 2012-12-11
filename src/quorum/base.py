#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (C) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Flask Quorum.
#
# Hive Flask Quorum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Flask Quorum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Flask Quorum. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import logging

import session
import redisdb
import mongodb

def load(app, redis_session = False, mongo_database = None, name = None):
    debug = os.getenv("DEBUG", False)
    redis_url = os.getenv("REDISTOGO_URL", None)
    mongo_url = os.getenv("MONGOHQ_URL", None)
    if not debug and name: start_log(app, name)
    if redis_url: redisdb.url = redis_url
    if mongo_url: mongodb.url = mongo_url
    if redis_session: app.session_interface = session.RedisSessionInterface(url = redis_url)
    if mongo_database: mongodb.database = mongo_database

def start_log(app, name):
    if os.name == "nt": path_t = "%s"
    else: path_t = "/var/log/%s"
    path = path_t % name
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)
