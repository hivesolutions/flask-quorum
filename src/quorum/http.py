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
import types
import random
import string
import urllib
import urllib2

import exceptions

TIMEOUT = 60
""" The timeout in seconds to be used for the blocking
operations in the http connection """

RANGE = string.ascii_letters + string.digits
""" The range of characters that are going to be used in
the generation of the boundary value for the mime """

SEQUENCE_TYPES = (types.ListType, types.TupleType)
""" The sequence defining the various types that are
considered to be sequence based for python """

def try_auth(auth_callback, params):
    if not auth_callback: raise
    auth_callback(params)

def get(url, auth_callback = None, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _get(url, **kwargs)
        except urllib2.HTTPError, error:
            if error.code == 403 and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                raise

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def get_json(url, auth_callback = None, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _get_json(url, **kwargs)
        except urllib2.HTTPError, error:
            if error.code == 403 and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_s = json.loads(data_r)
                raise exceptions.JsonError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def post_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    mime = None,
    auth_callback = None,
    **kwargs
):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _post_json(
                url,
                data = data,
                data_j = data_j,
                data_m = data_m,
                mime = mime,
                **kwargs
            )
        except urllib2.HTTPError, error:
            if error.code == 403 and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_s = json.loads(data_r)
                raise exceptions.JsonError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def put_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    mime = None,
    auth_callback = None,
    **kwargs
):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _put_json(
                url,
                data = data,
                data_j = data_j,
                data_m = data_m,
                mime = mime,
                **kwargs
            )
        except urllib2.HTTPError, error:
            if error.code == 403 and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_s = json.loads(data_r)
                raise exceptions.JsonError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def delete_json(url, auth_callback = None, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _delete_json(url, **kwargs)
        except urllib2.HTTPError, error:
            if error.code == 403 and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_s = json.loads(data_r)
                raise exceptions.JsonError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def _get(url, **kwargs):
    values = kwargs or {}
    data = _urlencode(values)
    url = url + "?" + data
    response = urllib2.urlopen(url, timeout = TIMEOUT)
    contents = response.read()
    return contents

def _get_json(url, **kwargs):
    contents = _get(url, **kwargs)
    contents_s = json.loads(contents) if contents else None
    return contents_s

def _post_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    mime = None,
    **kwargs
):
    values = kwargs or {}
    data_e = _urlencode(values)

    if data:
        url = url + "?" + data_e
    elif data_j:
        data = json.dumps(data_j)
        url = url + "?" + data_e
        mime = mime or "application/json"
    elif data_m:
        url = url + "?" + data_e
        content_type, data = _encode_multipart(data_m, doseq = True)
        mime = mime or content_type
    elif data_e:
        data = data_e
        mime = mime or "application/x-www-form-urlencoded"

    headers = dict()
    if mime: headers["Content-Type"] = mime

    request = urllib2.Request(url, data, headers = headers)
    response = urllib2.urlopen(request, timeout = TIMEOUT)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def _put_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    mime = None,
    **kwargs
):
    values = kwargs or {}
    data_e = _urlencode(values)

    if data:
        url = url + "?" + data_e
    elif data_j:
        data = json.dumps(data_j)
        url = url + "?" + data_e
        mime = mime or "application/json"
    elif data_m:
        url = url + "?" + data_e
        content_type, data = _encode_multipart(data_m, doseq = True)
        mime = mime or content_type
    elif data_e:
        data = data_e
        mime = mime or "application/x-www-form-urlencoded"

    headers = dict()
    if mime: headers["Content-Type"] = mime

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url, data, headers = headers)
    request.get_method = lambda: "PUT"
    response = opener.open(request, timeout = TIMEOUT)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def _delete_json(url, **kwargs):
    values = kwargs or {}
    data = _urlencode(values)
    url = url + "?" + data
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url)
    request.get_method = lambda: "DELETE"
    response = opener.open(request, timeout = TIMEOUT)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def _urlencode(values):
    # creates the dictionary that will hold the final
    # dictionary of values (without the unset and´
    # invalid values)
    final = dict()

    # iterates over all the items in the values map to
    # try to filter the values that are not valid
    for key, value in values.iteritems():
        # creates the list that will hold the valid values
        # of the current key in iteration (sanitized values)
        _values = []

        # verifies the type of the current value and in case
        # it's sequence based converts it into a list using
        # the conversion method otherwise creates a new list
        # and includes the value in it
        value_t = type(value)
        if value_t in SEQUENCE_TYPES: value = list(value)
        else: value = [value]

        # iterates over all the values in the current sequence
        # and adds the valid values to the sanitized sequence
        for _value in value:
            if _value == None: continue
            _values.append(_value)

        # sets the sanitized list of values as the new value for
        # the key in the final dictionary of values
        final[key] = _values

    # runs the encoding with sequence support on the final map
    # of sanitized values and returns the encoded result to the
    # caller method as the encoded value
    return urllib.urlencode(final, doseq = True)

def _encode_multipart(fields, doseq = False):
    boundary = _create_boundary(fields, doseq = doseq)
    buffer = []

    for key, values in fields.iteritems():
        is_list = doseq and type(values) == types.ListType
        values = values if is_list else [values]

        for value in values:
            value_t = type(value)

            if value_t == types.TupleType: is_file = True
            else: is_file = False

            if is_file:
                header = "Content-Disposition: form-data; name=\"%s\"; filename=\"%s\"" %\
                    (key, value[0])
                value = value[1]
            else:
                header = "Content-Disposition: form-data; name=\"%s\"" % key
                value = unicode(value).encode("utf-8")

            buffer.append("--" + boundary)
            buffer.append(header)
            buffer.append("")
            buffer.append(value)

    buffer.append("--" + boundary + "--")
    buffer.append("")
    body = "\r\n".join(buffer)
    content_type = "multipart/form-data; boundary=%s" % boundary

    return content_type, body

def _create_boundary(fields, size = 32, doseq = False):
    while True:
        base = "".join(random.choice(RANGE) for _value in range(size))
        boundary = "----------" + base
        result = _try_boundary(fields, boundary, doseq = doseq)
        if result: break

    return boundary

def _try_boundary(fields, boundary, doseq = False):
    for key, values in fields.iteritems():
        is_list = doseq and type(values) == types.ListType
        values = values if is_list else [values]

        for value in values:
            value_t = type(value)

            if value_t == types.TupleType: is_file = True
            else: is_file = False

            if is_file: name = value[0]; value = value[1]
            else: name = ""; value = unicode(value).encode("utf-8")

            if not key.find(boundary) == -1: return False
            if not name.find(boundary) == -1: return False
            if not value.find(boundary) == -1: return False

    return True
