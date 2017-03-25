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
import base64
import random
import string
import logging

from . import legacy
from . import typesf
from . import config
from . import common
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

AUTH_ERRORS = (401, 403, 440, 499)
""" The sequence that defines the various http errors
considered to be authentication related and for which a
new authentication try will be performed """

def try_auth(auth_callback, params, headers = None):
    if not auth_callback: raise
    if headers == None: headers = dict()
    auth_callback(params, headers)

def get_f(*args, **kwargs):
    name = kwargs.pop("name", "default")
    kwargs["handle"] = kwargs.get("handle", True)
    kwargs["redirect"] = kwargs.get("redirect", True)
    data, response = get_json(*args, **kwargs)
    info = response.info()
    mime = info.get("Content-Type", None)
    file_tuple = (name, mime, data)
    return typesf.File(file_tuple)

def get(url, auth_callback = None, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _get(url, **kwargs)
        except legacy.HTTPError as error:
            if error.code in AUTH_ERRORS and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                code = error.getcode()
                raise exceptions.HTTPDataError(error, code)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HTTPError("Data retrieval not possible")

def get_json(
    url,
    headers = None,
    handle = None,
    redirect = None,
    silent = None,
    timeout = None,
    auth_callback = None,
    **kwargs
):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _get_json(
                url,
                headers = headers,
                handle = handle,
                silent = silent,
                redirect = redirect,
                timeout = timeout,
                **kwargs
            )
        except legacy.HTTPError as error:
            if error.code in AUTH_ERRORS and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_r = legacy.str(data_r, encoding = "utf-8")
                data_s = json.loads(data_r)
                raise exceptions.JSONError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HTTPError("Data retrieval not possible")

def post_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
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
                handle = handle,
                silent = silent,
                redirect = redirect,
                timeout = timeout,
                **kwargs
            )
        except legacy.HTTPError as error:
            if error.code in AUTH_ERRORS and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_r = legacy.str(data_r, encoding = "utf-8")
                data_s = json.loads(data_r)
                raise exceptions.JSONError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HTTPError("Data retrieval not possible")

def put_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
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
                handle = handle,
                silent = silent,
                redirect = redirect,
                timeout = timeout,
                **kwargs
            )
        except legacy.HTTPError as error:
            if error.code in AUTH_ERRORS and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_r = legacy.str(data_r, encoding = "utf-8")
                data_s = json.loads(data_r)
                raise exceptions.JSONError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HTTPError("Data retrieval not possible")

def delete_json(
    url,
    headers = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
    auth_callback = None,
    **kwargs
):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _delete_json(
                url,
                headers = headers,
                handle = handle,
                silent = silent,
                redirect = redirect,
                timeout = timeout,
                **kwargs
            )
        except legacy.HTTPError as error:
            if error.code in AUTH_ERRORS and auth_callback:
                try_auth(auth_callback, kwargs)
            else:
                data_r = error.read()
                data_r = legacy.str(data_r, encoding = "utf-8")
                data_s = json.loads(data_r)
                raise exceptions.JSONError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HTTPError("Data retrieval not possible")

def _get(url, **kwargs):
    values = kwargs or dict()
    data = _urlencode(values)
    url = url + "?" + data if data else url
    file = _resolve(url, "GET", {}, None, False, TIMEOUT)
    contents = file.read()
    return contents

def _get_json(
    url,
    headers = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
    **kwargs
):
    return _method_empty(
        "GET",
        url,
        headers = headers,
        handle = handle,
        silent = silent,
        redirect = redirect,
        timeout = timeout,
        **kwargs
    )

def _post_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
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
        handle = handle,
        silent = silent,
        redirect = redirect,
        timeout = timeout,
        **kwargs
    )

def _put_json(
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
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
        handle = handle,
        silent = silent,
        redirect = redirect,
        timeout = timeout,
        **kwargs
    )

def _delete_json(
    url,
    headers = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
    **kwargs
):
    return _method_empty(
        "DELETE",
        url,
        headers = headers,
        handle = handle,
        silent = silent,
        redirect = redirect,
        timeout = timeout,
        **kwargs
    )

def _method_empty(
    name,
    url,
    headers = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
    **kwargs
):
    if handle == None: handle = False
    if silent == None: silent = False
    if redirect == None: redirect = False
    if timeout == None: timeout = TIMEOUT
    values = kwargs or dict()
    url, scheme, host, authorization, extra = _parse_url(url)
    if extra: values.update(extra)
    data = _urlencode(values)
    headers = dict(headers) if headers else dict()
    if host: headers["host"] = host
    if authorization: headers["Authorization"] = "Basic %s" % authorization
    url = url + "?" + data if data else url
    url = str(url)
    file = _resolve(url, name, headers, None, silent, timeout)
    try: result = file.read()
    finally: file.close()
    info = file.info()
    location = info.get("Location", None) if redirect else None
    if location: return _redirect(
        location,
        scheme,
        host,
        handle = handle,
        silent = silent,
        redirect = redirect,
        timeout = timeout
    )
    return (result, file) if handle else result

def _method_payload(
    name,
    url,
    data = None,
    data_j = None,
    data_m = None,
    headers = None,
    mime = None,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None,
    **kwargs
):
    if handle == None: handle = False
    if silent == None: silent = False
    if redirect == None: redirect = False
    if timeout == None: timeout = TIMEOUT
    values = kwargs or dict()

    url, scheme, host, authorization, extra = _parse_url(url)
    if extra: values.update(extra)
    data_e = _urlencode(values)

    if not data == None:
        url = url + "?" + data_e if data_e else url
    elif not data_j == None:
        data = json.dumps(data_j)
        url = url + "?" + data_e if data_e else url
        mime = mime or "application/json"
    elif not data_m == None:
        url = url + "?" + data_e if data_e else url
        content_type, data = _encode_multipart(
            data_m, mime = mime, doseq = True
        )
        mime = content_type
    elif data_e:
        data = data_e
        mime = mime or "application/x-www-form-urlencoded"

    data = legacy.bytes(data)
    length = len(data) if data else 0

    headers = dict(headers) if headers else dict()
    headers["Content-Length"] = length
    if mime: headers["Content-Type"] = mime
    if host: headers["Host"] = host
    if authorization: headers["Authorization"] = "Basic %s" % authorization
    url = str(url)

    file = _resolve(url, name, headers, data, silent, timeout)
    try: result = file.read()
    finally: file.close()

    info = file.info()

    location = info.get("Location", None) if redirect else None
    if location: return _redirect(
        location,
        scheme,
        host,
        handle = handle,
        silent = silent,
        redirect = redirect,
        timeout = timeout
    )

    return (result, file) if handle else result

def _redirect(
    location,
    scheme,
    host,
    handle = None,
    silent = None,
    redirect = None,
    timeout = None
):
    is_relative = location.startswith("/")
    if is_relative: location = scheme + "://" + host + location
    return get_json(
        location,
        handle = handle,
        silent = silent,
        redirect = redirect,
        timeout = timeout
    )

def _resolve(*args, **kwargs):
    # obtains the reference to the global set of variables, so
    # that it's possible to obtain the proper resolver method
    # according to the requested client
    _global = globals()

    # tries to retrieve the global configuration values that
    # will condition the way the request is going to be performed
    client = config.conf("HTTP_CLIENT", "netius")

    # tries to determine the set of configurations requested on
    # a request basis (not global) these have priority when
    # compared with the global configuration ones
    client = kwargs.pop("client", client)

    # tries to retrieve the reference to the resolve method for the
    # current client and then runs it, retrieve then the final result,
    # note that the result structure may be engine dependent
    resolver = _global.get("_resolve_" + client, _resolve_legacy)
    try: result = resolver(*args, **kwargs)
    except ImportError: result = _resolve_legacy(*args, **kwargs)
    return result

def _resolve_legacy(url, method, headers, data, silent, timeout, **kwargs):
    opener = legacy.build_opener(legacy.HTTPHandler)
    request = legacy.Request(url, data = data, headers = headers)
    request.get_method = lambda: method
    return opener.open(request, timeout = timeout)

def _resolve_requests(url, method, headers, data, silent, timeout, **kwargs):
    import requests
    method = method.lower()
    caller = getattr(requests, method)
    result = caller(url, headers = headers, data = data, timeout = timeout)
    response = HTTPResponse(
        data = result.content,
        code = result.status_code,
        headers = result.headers
    )
    code = response.getcode()
    is_error = _is_error(code)
    if is_error: raise legacy.HTTPError(
        url, code, "HTTP retrieval problem", None, response
    )
    return response

def _resolve_netius(url, method, headers, data, silent, timeout, **kwargs):
    import netius.clients
    silent = silent or False
    silent |= not common.is_devel()
    level = logging.CRITICAL if silent else logging.DEBUG
    level = kwargs.get("level", level)
    result = netius.clients.HTTPClient.method_s(
        method,
        url,
        headers = headers,
        data = data,
        async = False,
        timeout = timeout,
        level = level
    )
    response = netius.clients.HTTPClient.to_response(result)
    code = response.getcode()
    is_error = _is_error(code)
    if is_error: raise legacy.HTTPError(
        url, code, "HTTP retrieval problem", None, response
    )
    return response

def _parse_url(url):
    parse = legacy.urlparse(url)
    scheme = parse.scheme
    secure = scheme == "https"
    default = 443 if secure else 80
    port = parse.port or default
    url = parse.scheme + "://" + parse.hostname + ":" + str(port) + parse.path
    if port in (80, 443): host = parse.hostname
    else: host = parse.hostname + ":" + str(port)
    username = parse.username
    password = parse.password
    authorization = _authorization(username, password)
    params = _params(parse.query)
    return (url, scheme, host, authorization, params)

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

def _params(query):
    # creates the dictionary that is going to be used to store the
    # complete information regarding the parameters in query
    params = dict()

    # validates that the provided query value is valid and if
    # that's not the case returns the created parameters immediately
    # (empty parameters are returned)
    if not query: return params

    # splits the query value around the initial parameter separator
    # symbol and iterates over each of them to parse them and create
    # the proper parameters dictionary (of lists)
    query_s = query.split("&")
    for part in query_s:
        parts = part.split("=", 1)
        if len(parts) == 1: value = ""
        else: value = parts[1]
        key = parts[0]
        key = legacy.unquote_plus(key)
        value = legacy.unquote_plus(value)
        param = params.get(key, [])
        param.append(value)
        params[key] = param

    # returns the final parameters dictionary to the caller method
    # so that it may be used as a proper structure representation
    return params

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

def _authorization(username, password):
    if not username: return None
    if not password: return None
    payload = "%s:%s" % (username, password)
    payload = legacy.bytes(payload)
    authorization = base64.b64encode(payload)
    authorization = legacy.str(authorization)
    return authorization

def _encode_multipart(fields, mime = None, doseq = False):
    mime = mime or "multipart/form-data"
    boundary = _create_boundary(fields, doseq = doseq)
    boundary_b = legacy.bytes(boundary)

    buffer = []

    for key, values in fields.items():
        is_list = doseq and type(values) == list
        values = values if is_list else [values]

        for value in values:

            if isinstance(value, dict):
                header_l = []
                data = None
                for key, item in value.items():
                    if key == "data": data = item
                    else: header_l.append("%s: %s" % (key, item))
                value = data
                header = "\r\n".join(header_l)
            elif isinstance(value, tuple):
                content_type = None
                if len(value) == 2: name, contents = value
                else: name, content_type, contents = value
                header = "Content-Disposition: form-data; name=\"%s\"; filename=\"%s\"" %\
                    (key, name)
                if content_type: header += "\r\nContent-Type: %s" % content_type
                value = contents
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
    content_type = "%s; boundary=%s" % (mime, boundary)

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
            if isinstance(value, dict): name = ""; value = value.get("data", b"")
            elif isinstance(value, tuple): name = value[0] or ""; value = value[1]
            else: name = ""; value = _encode(value)

            if not key.find(boundary) == -1: return False
            if not name.find(boundary) == -1: return False
            if not value.find(boundary_b) == -1: return False

    return True

def _is_error(code):
    return code // 100 in (4, 5) if code else True

def _encode(value, encoding = "utf-8"):
    value_t = type(value)
    if value_t == legacy.BYTES: return value
    elif value_t == legacy.UNICODE: return value.encode(encoding)
    return legacy.bytes(str(value))

class HTTPResponse(object):
    """
    Compatibility object to be used by HTTP libraries that do
    not support the legacy HTTP response object as a return
    for any of their structures.
    """

    def __init__(self, data = None, code = 200, status = None, headers = None):
        self.data = data
        self.code = code
        self.status = status
        self.headers = headers

    def read(self):
        return self.data

    def readline(self):
        return self.read()

    def close(self):
        pass

    def getcode(self):
        return self.code

    def info(self):
        return self.headers
