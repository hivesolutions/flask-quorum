#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json
import flask
import functools

from . import log

SEQUENCE_TYPES = (list, tuple)
""" The tuple defining the various data types in
python that are considered to be representing a
logical sequence """

def check_basic_auth(username, password):
    authorization = flask.request.authorization
    if not authorization: return False
    if not authorization.username == username: return False
    if not authorization.password == password: return False
    return True

def check_login(token = None):
    # retrieves the data type of the token and creates the
    # tokens sequence value taking into account its type
    token_type = type(token)
    if token_type in SEQUENCE_TYPES: tokens = token
    else: tokens = (token,)

    # in case the username value is set in session and there's
    # no token to be validated returns valid and in case the checking
    # of the complete set of tokens is valid also returns valid
    if "username" in flask.session and not token: return True
    if check_tokens(tokens): return True

    # returns the default value as valid because if all the
    # validation procedures have passed the check is valid
    return True

def check_token(token, tokens_m = None):
    # tries to retrieve the tokens map from the provided argument
    # defaulting to the session one in case none is provided
    if tokens_m == None: tokens_m = get_tokens_m()

    # splits the provided token string into its parts, note that
    # a namespace is defined around the dot character
    token_l = token.split(".")

    # iterates over the complete set of parts in the token list
    # of parts to validate the complete chain of values against
    # the map of token parts (namespace validation)
    for token_p in token_l:
        if "*" in tokens_m and tokens_m["*"] == True: return True
        if not token_p in tokens_m: return False
        tokens_m = tokens_m[token_p]

    # verifies if the "final" tokens map value is valid and returns
    # the final validation result accordingly
    return True if tokens_m == True else False

def check_tokens(tokens, tokens_m = None):
    # iterates over the complete set of tokens that are going
    # to be validated against the current context and if any of
    # them fails an invalid result is returned otherwise a valid
    # result is returned (indicating that all is valid)
    for token in tokens:
        if not check_token(token, tokens_m = tokens_m): return False
    return True

def ensure_basic_auth(username, password, json_s = False):
    check = check_basic_auth(username, password)
    if check: return

    log.info("Unauthorized for operation")

    if json_s: return flask.Response(
            json.dumps({
                "exception" : {
                    "message" : "Unauthorized for operation"
                }
            }),
            status = 401,
            mimetype = "application/json"
        )
    else:
        return flask.redirect(
            flask.url_for(
                "login",
                next = flask.request.path,
                error = "Session expired or invalid"
            )
        )

def ensure_login(token = None, json_s = False):
    if check_login(token = token): return None

    log.info("Not enough permissions for operation '%s'" % token)

    if json_s:
        return flask.Response(
            json.dumps({
                "exception" : {
                    "message" : "Not enough permissions for operation"
                }
            }),
            status = 403,
            mimetype = "application/json"
        )
    else:
        return flask.redirect(
            flask.url_for(
                "login",
                next = flask.request.path,
                error = "Session expired or invalid"
            )
        )

def ensure_user(username):
    _username = flask.session.get("username", None)
    if not _username == None and username == _username: return
    raise RuntimeError("Permission denied")

def ensure_session(object):
    if object.get("sesion_id", None) == flask.session.get("session_id", None): return
    raise RuntimeError("Permission denied")

def ensure(token = None, json = False):
    """
    Decorator that provides support for verifying the current
    session login and permission (token oriented).

    The basic (login) verification ensures that the username
    session variable is set to a not null value (user logged in).

    The optional token parameter may be used to enforce presence
    of the string in the tokens sequence contained in session.

    An optional json parameter may be set in case the return
    error value should be returned as a json response instead
    of the normal (default) login page redirection.

    :type token: String
    :param token: The string based token to be in the verification
    procedure, in case the value is not set only the basic login
    verification is done.
    :type json: bool
    :param json: Flag indicating id an eventual error should be
    serialized as json and returned or if a page redirection
    should be used instead (default behavior).
    """

    def decorator(function):

        @functools.wraps(function)
        def interceptor(*args, **kwargs):
            ensure = ensure_login(token, json)
            if ensure: return ensure
            return function(*args, **kwargs)

        return interceptor

    return decorator

def ensure_auth(username, password, json = False):
    """
    Decorator that provides support for verifying the current
    request basic authentication information for the provided
    username and password.

    An optional json parameter may be set in case the return
    error value should be returned as a json response instead
    of the normal (default) login page redirection.

    :type username: String
    :param username: The username to be used for the verification
    of the basic authentication.
    :type password: String
    :param password: The password value to be used for matching
    if the basic authentication values verification.
    :type json: bool
    :param json: Flag indicating id an eventual error should be
    serialized as json and returned or if a page redirection
    should be used instead (default behavior).
    :see: http://en.wikipedia.org/wiki/Basic_access_authentication
    """

    def decorator(function):

        @functools.wraps(function)
        def interceptor(*args, **kwargs):
            ensure = ensure_basic_auth(username, password, json)
            if ensure: return ensure
            return function(*args, **kwargs)

        return interceptor

    return decorator

def get_tokens_m(set = True):
    """
    Retrieves the map of tokens from the current session so that
    they can be used for proper acl validation.

    In case the current session contains a sequence based representation
    of the tokens they are converted to their equivalent map value.

    :type set: bool
    :param set: If the possible converted tokens list should be persisted
    into the current session.
    :rtype: Dictionary
    :return: The map of tokens to be used for acl validation.
    """

    # tries to retrieve the tokens map from the current session
    # and then verifies if the resulting value is either a map
    # or a sequence, going to be used for decisions
    tokens_m = flask.session.get("tokens", {})
    is_map = isinstance(tokens_m, dict)
    is_sequence = isinstance(tokens_m, (list, tuple))

    # if the tokens value is already a map then an immediate return
    # is going to be performed (it is a valid tokens map)
    if is_map: return tokens_m

    # in case the value present in the tokens value is a sequence
    # it must be properly converted into the equivalent map value
    if is_sequence:
        # sets the retrieve tokens map (that is indeed a sequence) as
        # the tokens sequence and create a new ma to be used as the
        # tokens map that is going to be created from the list
        tokens_s = tokens_m
        tokens_m = dict()

        # iterates over the complete set of tokens in the
        # sequence to properly add their namespace parts
        # to the tokens map (as specified)
        for token in tokens_s:
            tokens_c = tokens_m
            token_l = token.split(".")
            head, tail = token_l[:-1], token_l[-1]
            for token_p in head:
                current = tokens_c.get(token_p, {})
                is_dict = isinstance(current, dict)
                if not is_dict: current = dict()
                tokens_c[token_p] = current
                tokens_c = current
            tokens_c[tail] = True

        # in case the set flag is set the tokens map should
        # be set in the request session (may be dangerous)
        # and then returns the tokens map to the caller method
        if set: flask.session["tokens"] = tokens_m
        return tokens_m

    # returns the "default" empty tokens map as it was not possible
    # to retrieve any information regarding tokens from the
    # current context and environment
    return dict()
