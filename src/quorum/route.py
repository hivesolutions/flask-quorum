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
import types
import traceback

import log
import base
import model
import mongodb
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
    def _route(function):
        def _decorator(*args, **kwargs):
            try: result = function(*args, **kwargs)
            except exceptions.OperationalError, exception:
                # prints a warning message to the current logger about the exception
                # that is being handled, note that the traceback is also logger, allowing
                # further debugging information to be printed (extra traceability)
                log.info(
                    "Operational problem while routing request - %s" % unicode(exception),
                    log_trace = True
                )

                # retrieves the formatted version of the traceback information and then
                # splits this information into the various lines that are contained in it
                formatted = traceback.format_exc()
                lines = formatted.splitlines()

                # creates a new response object containing the information about the exception
                # this is going to include the proper exception message, code and also the set
                # of lines that compose the traceback of the exception
                return flask.Response(
                    json.dumps({
                        "exception" : {
                            "name" : exception.__class__.__name__,
                            "message" : exception.message,
                            "code" : exception.code,
                            "traceback" : lines
                        }
                    }),
                    status = exception.code,
                    mimetype = "application/json"
                )
            except BaseException, exception:
                # prints a warning message to the current logger about the exception
                # that is being handled, note that the traceback is also logger, allowing
                # further debugging information to be printed (extra traceability)
                log.warning(
                    "Problem while routing request - %s" % unicode(exception),
                    log_trace = True
                )

                # retrieves the formatted version of the traceback information and then
                # splits this information into the various lines that are contained in it
                formatted = traceback.format_exc()
                lines = formatted.splitlines()

                # creates the response object that is going to be returned to the client indicating
                # that an undefined exception has just been raised, note that the error code
                # is the internal server error one (undefined exception)
                return flask.Response(
                    json.dumps({
                        "exception" : {
                            "name" : exception.__class__.__name__,
                            "message" : str(exception),
                            "code" : 500,
                            "traceback" : lines
                        }
                    }),
                    status = 500,
                    mimetype = "application/json"
                )

            # retrieves the type for the result that was returned from the
            # concrete method and in case the result is either a mongo object,
            # a dictionary or a sequence it's serialized as json, then returns
            # the result to the caller method
            result_t = type(result)
            if isinstance(result, model.Model):
                result = flask.Response(
                    mongodb.dumps(result),
                    mimetype = "application/json"
                )
            elif mongodb.is_mongo(result):
                result = flask.Response(
                    mongodb.dumps(result),
                    mimetype = "application/json"
                )
            elif result_t in (types.DictType, types.ListType, types.TupleType, types.NoneType):
                result = flask.Response(
                    mongodb.dumps(result),
                    mimetype = "application/json"
                )
            return result

        # verifies if the base value is set in the function for such
        # situations (double decoration) the base value should be set
        # as the already existing base decorator method otherwise keeps
        # using the clojure based one
        has_base = hasattr(function, "_base")
        if has_base: base = function._base
        else: base = _decorator

        # updates the decorates with the base value, this is going to be
        # the clojure based new view function, then in case this is a new
        # decorator updates the name of the decorator name with the name
        # of the base function (view function) that is getting decorated
        # so that the original name persists (otherwise a problem would
        # occur in werkzeug)
        _decorator = base
        if not has_base:
            _decorator.__name__ = function.__name__

        # runs the decorator to create a new decorator and sets the base
        # value in it as the current base value so that it gets propagated
        # all the way to the top decorators in sequence (pile of decorators)
        decorated = decorator(_decorator)
        decorated._base = base
        return decorated

    return _route
