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

import json
import flask

import base
import exceptions

def route(*args, **kwargs):
    # verifies if the request decorator should be of type
    # json serializer in case it should not returns the old
    # route decorator (default behavior)
    is_json = kwargs.get("json", False)
    if not is_json: return base.APP.old_route(*args, **kwargs)

    # removes the json keyword argument from the list of arguments
    # (to avoid errors) and then calls the old route method to obtain
    # the "normal" decorator
    del kwargs["json"]
    decorator = base.APP.old_route(*args, **kwargs)

    # creates the "new" route decorator maker method that should
    # override the old one and create a new decorator that
    # serializes all the unhandled exceptions as json
    def _route(functione):
        def _decorator(*args, **kwargs):
            try: return functione(*args, **kwargs)
            except exceptions.OperationalError, exception:
                return flask.Response(
                    json.dumps({
                        "exception" : {
                            "name" : exception.__class__.__name__,
                            "message" : exception.message,
                            "code" : exception.code
                        }
                    }),
                    status = exception.code,
                    mimetype = "application/json"
                )
            except BaseException, exception:
                return flask.Response(
                    json.dumps({
                        "exception" : {
                            "name" : exception.__class__.__name__,
                            "message" : str(exception),
                            "code" : 500
                        }
                    }),
                    status = 500,
                    mimetype = "application/json"
                )

        return decorator(_decorator)

    return _route
