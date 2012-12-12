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

import copy
import json
import flask

def request_json(request = None):
    request = request or flask.request
    if "_data_j" in request.properties: return request.properties["_data_j"]

    # retrieves the current request data and tries to
    # "load" it as json data, in case it fails gracefully
    # handles the failure setting the value as an empty map
    data = request.data
    try: data_j = json.loads(data)
    except: data_j = {}
    request.properties["_data_j"] = data_j

    return data_j

def get_field(name, default = None):
    data_j = request_json()

    value = data_j.get(name, default)
    value = flask.request.files.get(name, value)
    value = flask.request.form.get(name, value)
    value = flask.request.args.get(name, value)

    return value

def get_object(object = None):
    # verifies if the provided object is valid in such case creates
    # a copy of it and uses it as the base object for validation
    # otherwise used an empty map (form validation)
    object = object and copy.copy(object) or {}

    # retrieves the current request data and tries to
    # "load" it as json data, in case it fails gracefully
    # handles the failure setting the value as an empty map
    data_j = request_json()

    for name, value in data_j.items(): object[name] = value
    for name, value in flask.request.files.items(): object[name] = value
    for name, value in flask.request.form.items(): object[name] = value
    for name, value in flask.request.args.items(): object[name] = value

    return object
