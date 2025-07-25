#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2025 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2025 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

from . import util
from . import exceptions

try:
    import pusher
except ImportError:
    pusher = None

pusher_c = None
""" The global pusher connection object to be used along
multiple communications from the server side, when a client
requests the pusher object this is the one returned (if cached) """

app_id = None
""" The identifier of the app to be used for the current global
pusher connection a private key and secret should exist for each
app id described """

key = None
""" The encryption key to be used for the communication channel it
should be shared between the subscriber and the publisher """

secret = None
""" The secret key value that should be used by the publisher to
authenticate it "against" the pusher service """

cluster = None
""" The cluster (datacenter) that should be used in the client
connection that is going to be established """


def get_pusher():
    global pusher_c
    if pusher_c:
        return pusher_c
    if pusher == None:
        raise exceptions.ModuleNotFound("pusher")
    kwargs = dict()
    if cluster:
        kwargs["cluster"] = cluster
    pusher_c = _pusher().Pusher(
        app_id=str(app_id), key=str(key), secret=str(secret), **kwargs
    )
    return pusher_c


def _pusher(verify=True):
    if verify:
        util.verify(
            not pusher == None,
            message="Pusher library not available",
            exception=exceptions.OperationalError,
        )
    return pusher
