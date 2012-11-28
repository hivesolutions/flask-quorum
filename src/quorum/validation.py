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

import sys
import flask

import mongo
import exceptions

def validate(name):
    # retrieves the caller frame and uses it to retrieve
    # the map of global variables for it
    caller = sys._getframe(1)
    caller_globals = caller.f_globals

    validate_method = caller_globals.get("_validate_" + name, None)
    methods = validate_method and validate_method() or []
    errors = []

    object = {}
    for name, value in flask.request.files.items(): object[name] = value
    for name, value in flask.request.form.items(): object[name] = value
    for name, value in flask.request.args.items(): object[name] = value

    for method in methods:
        try: method()
        except exceptions.ValidationError, error:
            errors.append((error.name, error.message))

    errors_map = {}
    for name, message in errors:
        if not name in errors_map: errors_map[name] = []
        _errors = errors_map[name]
        _errors.append(message)

    return errors_map, object

def not_null(name):
    def validation():
        value = flask.request.args.get(
            name, flask.request.form.get(name, None)
        )
        if not value == None: return True
        raise exceptions.ValidationError(name, "value is not set")
    return validation

def not_empty(name):
    def validation():
        value = flask.request.args.get(
            name, flask.request.form.get(name, None)
        )
        if len(value): return True
        raise exceptions.ValidationError(name, "value is empty")
    return validation

def equals(first_name, second_name):
    def validation():
        first_value = flask.request.args.get(
            first_name, flask.request.form.get(first_name, None)
        )
        second_value = flask.request.args.get(
            second_name, flask.request.form.get(second_name, None)
        )
        if first_value == second_value: return True
        raise exceptions.ValidationError(first_name, "value is not equals")
    return validation

def not_duplicate(name, collection):
    def validation():
        _id = flask.request.args.get(
            "_id", flask.request.form.get("_id", None)
        )
        value = flask.request.args.get(
            name, flask.request.form.get(name, None)
        )
        db = mongo.get_db()
        _collection = db[collection]
        item = _collection.find_one({name : value})
        if not item: return True
        if str(item["_id"]) == _id: return True
        raise exceptions.ValidationError(name, "value is duplicate")
    return validation
