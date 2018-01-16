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

from . import util
from . import legacy
from . import exceptions

try: import pika
except: pika = None

TIMEOUT = 100
""" The time the retrieval of a connection waits before
returning this avoid possible problems with the current
implementation of the blocking client """

connection = None
""" The global wide connection to the AMQP server
that is meant to be used across sessions """

url = "amqp://guest:guest@localhost"
""" The global variable containing the URL to be used
for the connection with the service """

def get_connection(force = False, timeout = TIMEOUT):
    global connection
    if pika == None: raise exceptions.ModuleNotFound("pika")
    if not force and connection: return connection
    url_p = legacy.urlparse(url)
    parameters = _pika().ConnectionParameters(
        host = url_p.hostname,
        virtual_host = url_p.path or "/",
        credentials = _pika().PlainCredentials(url_p.username, url_p.password)
    )
    parameters.socket_timeout = timeout
    connection = _pika().BlockingConnection(parameters)
    connection = _set_fixes(connection)
    return connection

def properties(*args, **kwargs):
    return _pika().BasicProperties(*args, **kwargs)

def _set_fixes(connection):
    def disconnect():
        connection.socket.close()

    if not hasattr(connection, "disconnect"):
        connection.disconnect = disconnect
    return connection

def _pika(verify = True):
    if verify: util.verify(
        not pika == None,
        message = "pika library not available",
        exception = exceptions.OperationalError
    )
    return pika
