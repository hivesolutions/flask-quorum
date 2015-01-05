#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import json
import base64
import random
import string

from . import legacy
from . import config
from . import exceptions

TIMEOUT = 60
""" The timeout in seconds to be used for the blocking
operations in the http connection """

RANGE = string.ascii_letters + string.digits
""" The range of characters that are going to be used in
the generation of the boundary value for the mime """

SEQUENCE_TYPES = (list, tuple)
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
        except legacy.HTTPError as error:
            if error.code == 403 and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                raise

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def get_json(url, headers = None, auth_callback = None, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _get_json(url, headers = headers, **kwargs)
        except legacy.HTTPError as error:
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
    headers = None,
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
                headers = headers,
                mime = mime,
                **kwargs
            )
        except legacy.HTTPError as error:
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
    headers = None,
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
                headers = headers,
                mime = mime,
                **kwargs
            )
        except legacy.HTTPError as error:
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

def delete_json(url, headers = None, auth_callback = None, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _delete_json(url, headers = headers, **kwargs)
        except legacy.HTTPError as error:
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
    values = kwargs or dict()
    data = _urlencode(values)
    url = url + "?" + data if data else url
    file = _resolve(url, "GET", {}, None, TIMEOUT)
    contents = file.read()
    return contents

def _get_json(url, headers = None, **kwargs):
    return _method_empty("GET", url, headers = headers, **kwargs)

def _post_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    **kwargs
):
    return _method_payload(
        "POST",
        url,
        data = data,
        data_j = data_j,
        data_m = data_m,
        headers = headers,
        mime = mime,
        **kwargs
    )

def _put_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    **kwargs
):
    return _method_payload(
        "PUT",
        url,
        data = data,
        data_j = data_j,
        data_m = data_m,
        headers = headers,
        mime = mime,
        **kwargs
    )

def _delete_json(url, headers = None, **kwargs):
    return _method_empty("DELETE", url, headers = headers, **kwargs)

def _method_empty(name, url, headers = None, **kwargs):
    values = kwargs or dict()
    data = _urlencode(values)
    url, host, authorization = _parse_url(url)
    headers = headers or dict()
    if host: headers["host"] = host
    if authorization: headers["Authorization"] = "Basic %s" % authorization
    url = url + "?" + data if data else url
    url = str(url)
    file = _resolve(url, name, headers, None, TIMEOUT)
    try: result = file.read()
    finally: file.close()
    return _result(result, force = True)

def _method_payload(
    name,
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    **kwargs
):
    values = kwargs or dict()

    url, host, authorization = _parse_url(url)
    data_e = _urlencode(values)

    if data:
        url = url + "?" + data_e if data_e else url
    elif data_j:
        data = json.dumps(data_j)
        url = url + "?" + data_e if data_e else url
        mime = mime or "application/json"
    elif data_m:
        url = url + "?" + data_e if data_e else url
        content_type, data = _encode_multipart(data_m, doseq = True)
        mime = mime or content_type
    elif data_e:
        data = data_e
        mime = mime or "application/x-www-form-urlencoded"

    data = legacy.bytes(data)
    length = len(data) if data else 0

    headers = headers or dict()
    headers["Content-Length"] = length
    if mime: headers["Content-Type"] = mime
    if host: headers["Host"] = host
    if authorization: headers["Authorization"] = "Basic %s" % authorization
    url = str(url)

    file = _resolve(url, name, headers, data, TIMEOUT)
    try: result = file.read()
    finally: file.close()
    return _result(result, force = True)

def _resolve(*args, **kwargs):
    _global = globals()
    client = config.conf("HTTP_CLIENT", "netius")
    client = kwargs.get("client", client)
    if "client" in kwargs: del kwargs["client"]
    resolver = _global.get("_resolve_" + client, _resolve_base)
    try: result = resolver(*args, **kwargs)
    except ImportError: result = _resolve_base(*args, **kwargs)
    return result

def _resolve_base(url, method, headers, data, timeout):
    opener = legacy.build_opener(legacy.HTTPHandler)
    request = legacy.Request(url, data = data, headers = headers)
    request.get_method = lambda: method
    return opener.open(request, timeout = timeout)

def _resolve_netius(url, method, headers, data, timeout):
    import netius.clients
    result = netius.clients.HTTPClient.method_s(
        method,
        url,
        headers = headers,
        data = data,
        async = False
    )
    response = netius.clients.HTTPClient.to_response(result)
    code = response.getcode()
    is_error = code // 100 in (4, 5) if code else True
    if is_error: raise legacy.HTTPError(
        url, code, "HTTP retrieval problem", None, response
    )
    return response

def _parse_url(url):
    parse = legacy.urlparse(url)
    secure = parse.scheme == "https"
    default = 443 if secure else 80
    port = parse.port or default
    url = parse.scheme + "://" + parse.hostname + ":" + str(port) + parse.path
    if port in (80, 443): host = parse.hostname
    else: host = parse.hostname + ":" + str(port)
    username = parse.username
    password = parse.password
    if username and password:
        payload = "%s:%s" % (username, password)
        payload = legacy.bytes(payload)
        authorization = base64.b64encode(payload)
        authorization = legacy.str(authorization)
    else: authorization = None
    return (url, host, authorization)

def _result(data, info = {}, force = False, strict = False):
    # tries to retrieve the content type value from the headers
    # info and verifies if the current data is json encoded, so
    # that it gets automatically decoded for such cases
    content_type = info.get("Content-Type", None) or ""
    is_json = content_type.startswith((
        "application/json",
        "text/json",
        "text/javascript"
    )) or force

    # verifies if the current result set is json encoded and in
    # case it's decodes it and loads it as json otherwise returns
    # the "raw" data to the caller method as expected, note that
    # the strict flag is used to determine if the exception should
    # be re-raised to the upper level in case of value error
    if is_json and legacy.is_bytes(data): data = data.decode("utf-8")
    try: data = json.loads(data) if is_json else data
    except ValueError:
        if strict: raise
    return data

def _urlencode(values, as_string = True):
    # creates the dictionary that will hold the final
    # dictionary of values (without the unset andÂ´
    # invalid values)
    final = dict()

    # iterates over all the items in the values map to
    # try to filter the values that are not valid
    for key, value in values.items():
        # creates the list that will hold the valid values
        # of the current key in iteration (sanitized values)
        _values = []

        # in case the current data type of the key is unicode
        # the value must be converted into a string using the
        # default utf encoding strategy (as defined)
        if type(key) == legacy.UNICODE: key = key.encode("utf-8")

        # verifies the type of the current value and in case
        # it's sequence based converts it into a list using
        # the conversion method otherwise creates a new list
        # and includes the value in it
        value_t = type(value)
        if value_t in SEQUENCE_TYPES: value = list(value)
        else: value = [value]

        # iterates over all the values in the current sequence
        # and adds the valid values to the sanitized sequence,
        # this includes the conversion from unicode string into
        # a simple string using the default utf encoder
        for _value in value:
            if _value == None: continue
            is_string = type(_value) in legacy.STRINGS
            if not is_string: _value = str(_value)
            is_unicode = type(_value) == legacy.UNICODE
            if is_unicode: _value = _value.encode("utf-8")
            _values.append(_value)

        # sets the sanitized list of values as the new value for
        # the key in the final dictionary of values
        final[key] = _values

    # in case the "as string" flag is not set the ended key to value
    # dictionary should be returned to the called method and not the
    # "default" linear and string based value
    if not as_string: return final

    # runs the encoding with sequence support on the final map
    # of sanitized values and returns the encoded result to the
    # caller method as the encoded value
    return legacy.urlencode(final, doseq = True)

def _quote(values, plus = False, safe = "/"):
    method = legacy.quote_plus if plus else legacy.quote
    values = _urlencode(values, as_string = False)

    final = dict()

    for key, value in values.items():
        key = method(key, safe = safe)
        value = method(value[0], safe = safe)
        final[key] = value

    return final

def _encode_multipart(fields, doseq = False):
    boundary = _create_boundary(fields, doseq = doseq)
    boundary_b = legacy.bytes(boundary)

    buffer = []

    for key, values in fields.items():
        is_list = doseq and type(values) == list
        values = values if is_list else [values]

        for value in values:
            value_t = type(value)

            if value_t == tuple: is_file = True
            else: is_file = False

            if is_file:
                header = "Content-Disposition: form-data; name=\"%s\"; filename=\"%s\"" %\
                    (key, value[0])
                value = value[1]
            else:
                header = "Content-Disposition: form-data; name=\"%s\"" % key
                value = _encode(value)

            header = _encode(header)
            value = _encode(value)

            buffer.append(b"--" + boundary_b)
            buffer.append(header)
            buffer.append(b"")
            buffer.append(value)

    buffer.append(b"--" + boundary_b + b"--")
    buffer.append(b"")
    body = b"\r\n".join(buffer)
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
    boundary_b = legacy.bytes(boundary)

    for key, values in fields.items():
        is_list = doseq and type(values) == list
        values = values if is_list else [values]

        for value in values:
            value_t = type(value)

            if value_t == tuple: is_file = True
            else: is_file = False

            if is_file: name = value[0]; value = value[1]
            else: name = ""; value = _encode(value)

            if not key.find(boundary) == -1: return False
            if not name.find(boundary) == -1: return False
            if not value.find(boundary_b) == -1: return False

    return True

def _encode(value, encoding = "utf-8"):
    value_t = type(value)
    if value_t == legacy.BYTES: return value
    elif value_t == legacy.UNICODE: return value.encode(encoding)
    return legacy.bytes(str(value))
