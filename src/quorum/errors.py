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

import json
import flask
import functools

from . import exceptions


def errors_json(function):

    @functools.wraps(function)
    def interceptor(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except exceptions.ValidationError as error:
            invalid_m = {}
            for name, _errors in error.errors.items():
                invalid_m[name] = _errors[0]

            return flask.Response(
                json.dumps(
                    {
                        "error": error.message,
                        "invalid": invalid_m,
                        "exception": {"message": error.message, "errors": error.errors},
                    }
                ),
                status=error.code,
                mimetype="application/json",
            )
        except exceptions.OperationalError as error:
            return flask.Response(
                json.dumps(
                    {"error": error.message, "exception": {"message": error.message}}
                ),
                status=error.code,
                mimetype="application/json",
            )

    return interceptor
