#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import re
import sys
import copy
import json
import flask
import string
import locale
import random
import datetime
import itertools
import threading
import subprocess

import jinja2

from . import legacy
from . import common
from . import defines
from . import exceptions

FIRST_CAP_REGEX = re.compile("(.)([A-Z][a-z]+)")
""" Regular expression that ensures that the first
token of each camel string is properly capitalized """

ALL_CAP_REGEX = re.compile("([a-z0-9])([A-Z])")
""" The generalized transition from lower case to
upper case letter regex that will provide a way of
putting the underscore in the middle of the transition """

SORT_MAP = {
    "1" : 1,
    "-1" : -1,
    "ascending" : 1,
    "descending" : -1,
}
""" The map associating the normalized (text) way of
representing sorting with the current infra-structure
number way of representing the same information """

CASTERS = {
    list : lambda v: [y for y in itertools.chain(*[x.split(",") for x in v])],
    bool : lambda v: v if isinstance(v, bool) else\
        not v in ("", "0", "false", "False")
}
""" The map associating the various data types with a proper custom
caster to be used for special data types (more complex) under some
of the simple casting operations """

defines = defines

def to_limit(limit_s):
    limit = int(limit_s)
    if limit < 0: return 0
    return limit

def to_find(find_s):
    if not find_s: return []
    find_t = type(find_s)
    if find_t == list: return find_s
    return [find_s]

def to_sort(sort_s):
    values = sort_s.split(":", 1)
    if len(values) == 1: values.append("descending")
    name, direction = values
    if name == "default": return None
    values[1] = SORT_MAP.get(direction, 1)
    return [tuple(values)]

ALIAS = {
    "context" : "find_d",
    "filters" : "find_d",
    "filters[]" : "find_d",
    "filter_def" : "find_d",
    "filter_string" : "find_s",
    "filter_name" : "find_n",
    "insensitive" : "find_i",
    "order" : "sort",
    "offset" : "skip",
    "start_record" : "skip",
    "number_records" : "limit"
}
""" The map containing the various attribute alias
between the normalized manned and the quorum manner """

FIND_TYPES = dict(
    skip = int,
    limit = to_limit,
    find_s = legacy.UNICODE,
    find_d = to_find,
    find_i = bool,
    find_t = legacy.UNICODE,
    find_n = legacy.UNICODE,
    sort = to_sort,
    meta = bool,
    fields = list
)
""" The map associating the various find fields with
their respective types, note that in case a special
conversion operation is required the associated value
may represent a conversion function instead """

FIND_DEFAULTS = dict(
    limit = 10
)
""" The map that defines the various default values
for a series of find related attributes """

def is_iterable(object):
    return isinstance(object, defines.ITERABLES)

def request_json(request = None, encoding = "utf-8"):
    # retrieves the proper request object, either the provided
    # request or the default flask request object and then in
    # case the the json data is already in the request properties
    # it is used (cached value) otherwise continues with the parse
    request = request or flask.request
    try:
        if "_data_j" in request.properties:
            return request.properties["_data_j"]
    except RuntimeError: pass

    # retrieves the current request data and tries to
    # "load" it as json data, in case it fails gracefully
    # handles the failure setting the value as an empty map
    data = request.data
    try:
        is_bytes = legacy.is_bytes(data)
        if is_bytes: data = data.decode(encoding)
        data_j = json.loads(data)
    except: data_j = {}
    request.properties["_data_j"] = data_j

    # returns the json data object to the caller method so that it
    # may be used as the parsed value (post information)
    return data_j

def get_field(name, default = None, cast = None, strip = False):
    # tries to retrieve the json based representation of the provided
    # request from all the possible sources, this is required because
    # it's going to be used to try to retrieve a field from it
    data_j = request_json()

    # tries to retrieve the requested field from all the requested sources
    # the order of retrieval should respect the importance of each of the
    # sources (from the least important to the most important)
    value = data_j.get(name, default)
    value = flask.request.files.get(name, value)
    value = flask.request.form.get(name, value)
    value = flask.request.args.get(name, value)

    # in case the strip flag is enabled an "extra" strip operation is applied
    # to the retrieved value (as requested), avoiding extra spaces
    if strip: value = value.strip()

    # in case a cast operation is defined, tries to retrieve a possible
    # indirect/custom caster for the current cast operation
    if cast: cast = CASTERS.get(cast, cast)

    # in case the cast type value is set and the value is not invalid tries
    # to cast the value into the requested cast type
    if cast and not value in (None, ""): value = cast(value)

    # returns the final value to the caller method to be used, note that the
    # caller method should be aware of the sources used in the field retrieval
    return value

def get_object(
    object = None,
    alias = False,
    page = False,
    find = False,
    norm = True,
    **kwargs
):
    # verifies if the provided object is valid in such case creates
    # a copy of it and uses it as the base object for validation
    # otherwise used an empty map (form validation)
    object = object and copy.copy(object) or {}

    # retrieves the current request data and tries to
    # "load" it as json data, in case it fails gracefully
    # handles the failure setting the value as an empty map
    try: data_j = request_json()
    except RuntimeError: data_j = dict()

    # retrieves the reference to the file objects currently
    # present in the request, note that in case a runtime
    # error occurs (eg: out of context) fails gracefully
    try: files = flask.request.files
    except RuntimeError: files = dict()

    # retrieves the reference to the form objects currently
    # present in the request, note that in case a runtime
    # error occurs (eg: out of context) fails gracefully
    try: form_s = flask.request.form_s
    except RuntimeError: form_s = dict()

    # retrieves the reference to the arguments objects currently
    # present in the request, note that in case a runtime
    # error occurs (eg: out of context) fails gracefully
    try: args_s = flask.request.args_s
    except RuntimeError: args_s = dict()

    # uses all the values referencing data in the request to try
    # to populate the object this way it may be constructed using
    # any of theses strategies (easier for the developer)
    for name, value in data_j.items(): object[name] = value
    for name, value in files.items(): object[name] = value
    for name, value in form_s.items(): object[name] = value
    for name, value in args_s.items(): object[name] = value

    # in case the alias flag is set tries to resolve the attribute
    # alias and in case the find types are set converts the find
    # based attributes using the currently defined mapping map
    alias and resolve_alias(object)
    page and page_types(object)
    find and find_types(object)
    find and find_defaults(object, kwargs)

    # in case the normalization flag is set runs the normalization
    # of the provided object so that sequences are properly handled
    # as defined in the specification (this allows multiple references)
    norm and norm_object(object)

    # returns the constructed object to the caller method this object
    # should be a structured representation of the data in the request
    return object

def is_mobile(user_agent = None):
    """
    Verifies if the current user agent string represents a
    mobile agent, for that a series of regular expressions
    are matched against the user agent string.

    :type user_agent: String
    :param user_agent: The string containing the user agent
    value that is going to be verified against a series of
    regular expressions for mobile verification.
    :rtype: bool
    :return: If the current user agent string represents a
    mobile browser or a regular (desktop) one.
    """

    user_agent = flask.request.headers.get("User-Agent", "")\
        if user_agent == None else user_agent
    prefix = user_agent[:4]
    mobile = defines.MOBILE_REGEX.search(user_agent)
    mobile_prefix = defines.MOBILE_PREFIX_REGEX.search(prefix)
    is_mobile = True if mobile or mobile_prefix else False
    return is_mobile

def is_tablet(user_agent = None):
    """
    Verifies if the current user agent string represents a
    tablet agent, for that a series of regular expressions
    are matched against the user agent string.

    :type user_agent: String
    :param user_agent: The string containing the user agent
    value that is going to be verified against a series of
    regular expressions for tablet verification.
    :rtype: bool
    :return: If the current user agent string represents a
    tablet browser or a regular (desktop) one.
    """

    user_agent = flask.request.headers.get("User-Agent", "")\
        if user_agent == None else user_agent
    prefix = user_agent[:4]
    tablet = defines.TABLET_REGEX.search(user_agent)
    mobile_prefix = defines.MOBILE_PREFIX_REGEX.search(prefix)
    is_tablet = True if tablet or mobile_prefix else False
    return is_tablet

def is_browser(user_agent = None):
    """
    Verifies if the provided user agent string represents a
    browser (interactive) agent, for that a series of verifications
    are going to be performed against the user agent string.

    :type user_agent: String
    :param user_agent: The string containing the user agent
    value that is going to be verified for browser presence.
    :rtype: bool
    :return: If the provided user agent string represents an
    interactive browser or not.
    """

    user_agent = flask.request.headers.get("User-Agent", "")\
        if user_agent == None else user_agent
    info = browser_info(user_agent = user_agent)
    if not info: return False
    interactive = info.get("interactive", False)
    if not interactive: return False
    return True

def is_bot(user_agent = None):
    """
    Verifies if the provided user agent string represents a
    bot (automated) agent, for that a series of verifications
    are going to be performed against the user agent string.

    :type user_agent: String
    :param user_agent: The string containing the user agent
    value that is going to be verified for bot presence.
    :rtype: bool
    :return: If the provided user agent string represents an
    automated bot or not.
    """

    user_agent = flask.request.headers.get("User-Agent", "")\
        if user_agent == None else user_agent
    info = browser_info(user_agent = user_agent)
    if not info: return False
    bot = info.get("bot", False)
    if not bot: return False
    return True

def browser_info(user_agent = None):
    """
    Retrieves a dictionary containing information about the browser
    and the operative system associated with the provided user agent.

    The retrieval of the information depends on the kind of user
    agent string provided, as coverage is limited.

    :type user_agent: String
    :param user_agent: The HTTP based user agent string to be processed.
    :rtype: Dictionary
    :return: The dictionary/map containing the information processed from
    the provided user agent.
    """

    user_agent = flask.request.headers.get("User-Agent", "")\
        if user_agent == None else user_agent

    info = dict()

    for browser_i in defines.BROWSER_INFO:
        identity = browser_i["identity"]
        sub_string = browser_i.get("sub_string", identity)
        version_search = browser_i.get("version_search", sub_string + "/")
        interactive = browser_i.get("interactive", True)
        bot = browser_i.get("bot", False)

        if not sub_string in user_agent: continue
        if not version_search in user_agent: continue

        version_i = user_agent.index(version_search) + len(version_search)
        version = user_agent[version_i:].split(" ", 1)[0].strip(" ;")
        version_f = float(".".join(version.split(".")[:2]))
        version_i = int(version_f)

        info.update(
            name = identity,
            version = version,
            version_f = version_f,
            version_i = version_i,
            interactive = interactive,
            bot = bot
        )
        break

    for os_i in defines.OS_INFO:
        identity = os_i["identity"]
        sub_string = os_i.get("sub_string", identity)

        if not sub_string in user_agent: continue

        info.update(os = identity)
        break

    return info if info else None

def resolve_alias(object):
    for name, value in legacy.eager(object.items()):
        if not name in ALIAS: continue
        _alias = ALIAS[name]
        object[_alias] = value
        del object[name]

def page_types(object, size = 50):
    page = object.get("page", 1)
    size = object.get("size", size)
    sorter = object.get("sorter", None)
    direction = object.get("direction", "descending")
    page = int(page)
    size = int(size)
    offset = page - 1
    object["skip"] = offset * size
    object["limit"] = size
    if sorter: object["sort"] = "%s:%s" % (sorter, direction)

def find_types(object):
    # iterates over all the name and values of the object
    # trying to convert each of the find types into the
    # appropriate representation for the infra-structure
    for name, value in legacy.eager(object.items()):
        # in case the current find name is not present
        # in the find types map it's removed from the
        # object as it is considered to be invalid
        if not name in FIND_TYPES:
            del object[name]
            continue

        # retrieves the find (data) type associated with
        # the current find name and "runs" the conversion
        # method retrieving the resulting value
        find_type = FIND_TYPES[name]
        value = find_type(value)

        # in case the value resulting from the conversion
        # is invalid the name is removed from the find object
        # because it's not considered to be valid
        if value == None: del object[name]
        else: object[name] = value

def find_defaults(object, kwargs):
    for name, value in legacy.iteritems(kwargs):
        if name in object: continue
        if not name in FIND_TYPES: continue
        object[name] = value

    for name, value in legacy.iteritems(FIND_DEFAULTS):
        if name in object: continue
        object[name] = value

def norm_object(object):
    # iterates over all the key value association in the
    # object, trying to find the ones that refer sequences
    # so that they may be normalized
    for name, value in legacy.eager(object.items()):
        # verifies if the current name references a sequence
        # and if that's not the case continues the loop trying
        # to find any other sequence based value
        if not name.endswith("[]"): continue

        # removes the current reference to the name as the value
        # is not in the valid structure and then normalizes the
        # name by removing the extra sequence indication value
        del object[name]
        name = name[:-2]

        # in case the current value is not valid (empty) the object
        # is set with an empty list for the current iteration as this
        # is considered to be the default value
        if not value: object[name] = []; continue

        # retrieves the normalized and linearized list of leafs
        # for the current value and ten verifies the size of each
        # of its values and uses it to measure the number of
        # dictionary elements that are going to be contained in
        # the sequence to be "generated", then uses this (size)
        # value to pre-generate the complete set of dictionaries
        leafs_l = leafs(value)
        first = leafs_l[0] if leafs_l else (None, [])
        _fqn, values = first
        size = len(values)
        list = [dict() for _index in range(size)]

        # sets the list of generates dictionaries in the object for
        # the newly normalized name of structure
        object[name] = list

        # iterates over the complete set of key value pairs in the
        # leafs list to gather the value into the various objects that
        # are contained in the sequence (normalization process)
        for _name, _value in leafs_l:
            for index in range(size):
                _object = list[index]
                _name_l = _name.split(".")
                set_object(_object, _name_l, _value[index])

def set_object(object, name_l, value):
    """
    Sets a composite value in an object, allowing for
    dynamic setting of random size key values.

    This method is useful for situations where one wants
    to set a value at a randomly defined depth inside
    an object without having to much work with the creation
    of the inner dictionaries.

    :type object: Dictionary
    :param object: The target object that is going to be
    changed and set with the target value.
    :type name_l: List
    :param name_l: The list of names that defined the fully
    qualified name to be used in the setting of the value
    for example path.to.end will be a three size list containing
    each of the partial names.
    :type value: Object
    :param value: The value that is going to be set in the
    defined target of the object.
    """

    # retrieves the first name in the names list this is the
    # value that is going to be used for the current iteration
    name = name_l[0]

    # in case the length of the current names list has reached
    # one this is the final iteration and so the value is set
    # at the current naming point
    if len(name_l) == 1: object[name] = value

    # otherwise this is a "normal" step and so a new map must
    # be created/retrieved and the iteration step should be
    # performed on this new map as it's set on the current naming
    # place (recursion step)
    else:
        map = object.get(name, {})
        object[name] = map
        set_object(map, name_l[1:], value)

def leafs(object):
    """
    Retrieves a list containing a series of tuples that
    each represent a leaf of the current object structure.

    A leaf is the last element of an object that is not a
    map, the other intermediary maps are considered to be
    trunks and should be percolated recursively.

    This is a recursive function that takes some memory for
    the construction of the list, and so should be used with
    the proper care to avoid bottlenecks.

    :type object: Dictionary
    :param object: The object for which the leafs list
    structure is meant to be retrieved.
    :rtype: List
    :return: The list of leaf node tuples for the provided
    object, as requested for each of the sequences.
    """

    # creates the list that will hold the various leaf nodes
    # "gathered" by the current recursion function
    leafs_l = []

    # iterates over all the key and value relations in the
    # object trying to find the leaf nodes (no map nodes)
    # creating a tuple of fqn (fully qualified name) and value
    for name, value in object.items():
        # retrieves the data type for the current value and
        # validation if it is a dictionary or any other type
        # in case it's a dictionary a new iteration step must
        # be performed retrieving the leafs of the value and
        # then incrementing the name with the current prefix
        value_t = type(value)
        if value_t == dict:
            _leafs = leafs(value)
            _leafs = [(name + "." + _name, value) for _name, value in _leafs]
            leafs_l.extend(_leafs)

        # otherwise this is a leaf node and so the leaf tuple
        # node must be constructed with the current value
        # (properly validated for sequence presence)
        else:
            value_t = type(value)
            if not value_t == list: value = [value]
            leafs_l.append((name, value))

    # returns the list of leaf nodes that was "just" created
    # to the caller method so that it may be used there
    return leafs_l

def load_form(form):
    # creates the map that is going to hold the "structured"
    # version of the form with key value associations
    form_s = dict()

    # iterates over all the form items to parse their values
    # and populate the form structured version of it, note that
    # for the sake of parsing the order of the elements in the
    # form is relevant, in case there's multiple values for the
    # same name they are considered as a list, otherwise they are
    # considered as a single value
    for name in form:
        # retrieves the value (as a list) for the current name, then
        # in case the sequence is larger than one element sets it,
        # otherwise retrieves and sets the value as the first element
        value = form.getlist(name)
        value = value[0] if isinstance(value, (list, tuple)) and\
            len(value) == 1 else value

        # splits the complete name into its various components
        # and retrieves both the final (last) element and the
        # various partial elements from it
        names = name.split(".")
        final = names[-1]
        partials = names[:-1]

        # sets the initial "struct" reference as the form structured
        # that has just been created (initial structure for iteration)
        # then starts the iteration to retrieve or create the various
        # intermediate structures
        struct = form_s
        for _name in partials:
            _struct = struct.get(_name, {})
            struct[_name] = _struct
            struct = _struct

        # sets the current value in the currently loaded "struct" element
        # so that the reference gets properly updated
        struct[final] = value

    # retrieves the final "normalized" form structure containing
    # a series of chained maps resulting from the parsing of the
    # linear version of the attribute names
    return form_s

def load_locale(available, fallback = "en_us"):
    # tries to gather the best locale value using the currently
    # available strategies and in case the retrieved local is part
    # of the valid locales for the app returns the locale, otherwise
    # returns the fallback value instead
    locale = get_locale(fallback = fallback)
    if locale in available: return locale
    return fallback

def get_locale(fallback = "en_us"):
    # tries to retrieve the locale value from the provided URL
    # parameters (this is the highest priority) and in case it
    # exists returns this locale immediately
    locale = flask.request.args.get("locale", None)
    if locale: return locale

    # uses the currently loaded session to try to gather the locale
    # value from it and in case it's valid and exists returns it
    locale = flask.session.get("locale", None)
    if locale: return locale

    # gathers the complete set of language values set in the accept
    # language header and in case there's at least one value returned
    # returns the first of these values as the locale
    langs = get_langs()
    if langs: return langs[0]

    # in case this code entry is reached all the strategies for locale
    # retrieval have failed and so the fallback value is returned
    return fallback

def get_langs():
    # gathers the value of the accept language header and in case
    # it's not defined returns immediately as no language can be
    # determined using the currently provided headers
    accept_language = flask.request.headers.get("Accept-Language", None)
    if not accept_language: return ()

    # starts the list that is going to be used to store the various
    # languages "recovered" from the accept language header, note that
    # the order of these languages should be from the most relevant to
    # the least relevant as defined in http specification
    langs = []

    # splits the accept language header into the various components of
    # it and then iterates over each of them splitting each of the
    # components into the proper language string and priority
    parts = accept_language.split(",")
    for part in parts:
        values = part.split(";", 1)
        value_l = len(values)
        if value_l == 1: lang, = values
        else: lang, _priority = values
        lang = lang.replace("-", "_")
        lang = lang.lower()
        langs.append(lang)

    # returns the complete list of languages that have been extracted
    # from the accept language header these list may be empty in case
    # the header was not parsed correctly or there's no contents in it
    return langs

def set_locale():
    # normalizes the current locale string by converting the
    # last part of the locale string to an uppercase representation
    # and then re-joining the various components of it
    values = flask.request.locale.split("_", 1)
    if len(values) > 1: values[1] = values[1].upper()
    locale_n = "_".join(values)
    locale_n = str(locale_n)

    # in case the current operative system is windows based an
    # extra locale conversion operation must be performed, after
    # than the proper setting of the os locale is done with the
    # fallback for exception being silent (non critical)
    if os.name == "nt": locale_n = defines.WINDOWS_LOCALE.get(locale_n, "")
    else: locale_n += ".utf8"
    try: locale.setlocale(locale.LC_ALL, locale_n)
    except: pass

def reset_locale():
    locale.setlocale(locale.LC_ALL, "")

def anotate_async(response):
    # verifies if the current response contains the location header
    # meaning that a redirection will occur, and if that's not the
    # case this function returns immediately to avoid problems
    if not "Location" in response.headers: return

    # checks if the current request is "marked" as asynchronous, for
    # such cases a special redirection process is applies to avoid the
    # typical problems with automated redirection using "ajax"
    is_async = True if flask.request.headers.get("X-Async") else False
    is_async = True if get_field("async") else is_async
    if is_async: response.status_code = 280

def run_thread(function, *args, **kwargs):
    return threading.Thread(
        target = function,
        args = args,
        kwargs = kwargs
    ).start()

def camel_to_underscore(camel, separator = "_", lower = True):
    """
    Converts the provided camel cased based value into
    a normalized underscore based string.

    An optional lower parameter may be used to avoid the case
    of the letters from being lower cased.

    This is useful as most of the python string standards
    are compliant with the underscore strategy.

    :type camel: String
    :param camel: The camel cased string that is going to be
    converted into an underscore based string.
    :type separator: String
    :param separator: The separator token that is going to
    be used in the camel to underscore conversion.
    :type lower: bool
    :param lower: If the letter casing should be changed while
    convert the value from camel to underscore.
    :rtype: String
    :return: The underscore based string resulting from the
    conversion of the provided camel cased one.
    """

    value = FIRST_CAP_REGEX.sub(r"\1" + separator + r"\2", camel)
    value = ALL_CAP_REGEX.sub(r"\1" + separator + r"\2", value)
    if lower: value = value.lower()
    return value

def camel_to_readable(camel, lower = False, capitalize = False):
    """
    Converts the given camel cased oriented string value
    into a readable one meaning that the returned value
    is a set of strings separated by spaces.

    This method may be used to convert class names into
    something that is readable by an end user.

    :type camel: String
    :param camel: The camel case string value that is going
    to be used in the conversion into a readable string.
    :type lower: bool
    :param lower: If the camel based value should be lower
    cased before the conversion to readable.
    :type capitalize: bool
    :param capitalize: If all of the words should be capitalized
    or if instead only the first one should.
    :rtype: String
    :return: The final human readable string that may be
    used to display a value to an end user.
    """

    underscore = camel_to_underscore(camel, lower = lower)
    return underscore_to_readable(underscore, capitalize = capitalize)

def underscore_to_readable(underscore, capitalize = False):
    """
    Converts the given underscore oriented string value
    into a readable one meaning that the returned value
    is a set of strings separated by spaces.

    This method may be used to class attributes into
    something that is readable by an end user.

    :type camel: String
    :param camel: The underscore string value that is going
    to be used in the conversion into a readable string.
    :type capitalize: bool
    :param capitalize: If all of the words should be capitalized
    or if instead only the first one should.
    :rtype: String
    :return: The final human readable string that may be
    used to display a value to an end user.
    """

    parts = underscore.split("_")
    if capitalize: parts = [part[0].upper() + part[1:] for part in parts]
    else: parts[0] = parts[0][0].upper() + parts[0][1:]
    return " ".join(parts)

def generate_identifier(size = 16, chars = string.ascii_uppercase + string.digits):
    """
    Generates a random identifier (may be used as password) with
    the provided constrains of length and character ranges.

    This function may be used in the generation of random based
    keys for both passwords and api keys.

    :type size: int
    :param size: The size (in number of characters) to be used in
    the generation of the random identifier.
    :type chars: List
    :param chars: The list containing the characters to be used
    in the generation of the random identifier.
    :rtype: String
    :return: The randomly generated identifier obeying to the
    provided constrains.
    """

    return "".join(random.choice(chars) for _index in range(size))

def to_locale(value, locale = None, fallback = True):
    """
    Utility function used to localize the provided value according
    to the currently loaded set of bundles, the bundles are loaded
    at the application start time from the proper sources.

    The (target) locale value for the translation may be provided or
    in case it's not the locale associated with the current request
    is used as an alternative.

    In case the value is not localizable (no valid bundle available)
    it is returned as it is without change.

    :type value: String
    :param value: The value that is going to be localized according
    to the current application environment, this may be a normal
    english dictionary string or a variable reference.
    :type locale: String
    :param locale: The (target) locale value to be used in the
    translation process for the provided string value.
    :type fallback: bool
    :param fallback: If a fallback operation should be performed in
    case no value was retrieved from the base/request locale.
    :rtype: String
    :return: The localized value for the current environment or the
    proper (original) value in case no localization was possible.
    """

    value_t = type(value)
    is_sequence = value_t in (list, tuple)
    if is_sequence: return _serialize([
        to_locale(value, locale = locale, fallback = fallback)\
        for value in value
    ])
    has_context = common.base().has_context()
    locale = locale or (flask.request.locale if has_context else None)
    bundle = common.base().get_bundle(locale) or {}
    result = bundle.get(value, None)
    if not result == None: return result
    app = common.base().APP
    if fallback and app: return to_locale(
        value,
        locale = app._locale_d,
        fallback = False
    )
    return value

def nl_to_br(value):
    """
    Replaces the occurrences of the newline character in the
    string with the HTML break line character.

    This is useful for one trying to convert a plain text
    representation of a string into HTML representation.

    :type value: String
    :param value: The base value that is going to be used in
    the conversion to the HTML value.
    :rtype: String
    :return: The string containing the newline characters replaced
    with line breaking HTML tags.
    """

    return value.replace("\n", "<br/>\n")

def nl_to_br_jinja(eval_ctx, value):
    """
    Optimized version of the function that replaces newline
    characters with the HTML break lines that handles the
    autoescape properties of the jinja engine.

    :type eval_ctx: Context
    :param eval_ctx: Current evaluation context being used
    in the rendering of the jinja template. May be used to
    determine if the autoescape mode is being used.
    :type value: String
    :param value: The base value that is going to be used in
    the conversion to the html value.
    :rtype: String
    :return: The string containing the newline characters replaced
    with line breaking HTML tags.
    """

    if eval_ctx.autoescape: value = legacy.UNICODE(jinja2.escape(value))
    value = nl_to_br(value)
    if eval_ctx.autoescape: value = jinja2.Markup(value)
    return value

def sp_to_nbsp(value):
    """
    Replaces the occurrences of the space character in the
    string with the HTML non breaking space character.

    This is useful for one trying to convert a plain text
    representation of a string into HTML representation.

    :type value: String
    :param value: The base value that is going to be used in
    the conversion to the HTML value.
    :rtype: String
    :return: The string containing the space characters replaced
    with non breaking space characters for HTML.
    """

    return value.replace(" ", "&nbsp;")

def sp_to_nbsp_jinja(eval_ctx, value):
    """
    Optimized version of the function that replaces space
    characters with the HTML non breaking space characters
    that handles the autoescape properties of the jinja engine.

    :type eval_ctx: Context
    :param eval_ctx: Current evaluation context being used
    in the rendering of the jinja template. May be used to
    determine if the autoescape mode is being used.
    :type value: String
    :param value: The base value that is going to be used in
    the conversion to the HTML value.
    :rtype: String
    :return: The string containing the space characters replaced
    with non breaking space characters for HTML.
    """

    if eval_ctx.autoescape: value = legacy.UNICODE(jinja2.escape(value))
    value = sp_to_nbsp(value)
    if eval_ctx.autoescape: value = jinja2.Markup(value)
    return value

def date_time(value, format = "%d/%m/%Y"):
    """
    Formats the provided as a date string according to the
    provided date format.

    Assumes that the provided value represents a float string
    and that may be used as the based timestamp for conversion.

    :type value: String
    :param value: The base timestamp value string that is going
    to be used for the conversion of the date string.
    :type format: String
    :param format: The format string that is going to be used
    when formatting the date time value.
    :rtype: String
    :return: The resulting date time string that may be used
    to represent the provided value.
    """

    # tries to convert the provided string value into a float
    # in case it fails the proper string value is returned
    # immediately as a fallback procedure
    try: value_f = float(value)
    except: return value

    # creates the date time structure from the provided float
    # value and then formats the date time according to the
    # provided format and returns the resulting string
    date_time_s = datetime.datetime.utcfromtimestamp(value_f)
    return date_time_s.strftime(format).decode("utf-8")

def quote(value, *args, **kwargs):
    """
    Quotes the passed value according to the defined
    standard for url escaping, the value is first encoded
    into the expected utf-8 encoding as defined by standard.

    This method should be used instead of a direct call to
    the equivalent call in the URL library.

    :type value: String
    :param value: The string value that is going to be quoted
    according to the URL escaping scheme.
    :rtype: String
    :return: The quoted value according to the URL scheme this
    value may be safely used in urls.
    """

    is_unicode = isinstance(value, legacy.UNICODE)
    if is_unicode: value = value.encode("utf-8")
    return legacy.quote(value, *args, **kwargs)

def unquote(value, *args, **kwargs):
    """
    Unquotes the provided value according to the URL scheme
    the resulting value should be an unicode string representing
    the same value, the intermediary string value from the decoding
    should be an utf-8 based value.

    This method should be used instead of a direct call to
    the equivalent call in the URL library.

    :type value: String
    :param value: The string value that is going to be unquoted
    according to the URL escaping scheme.
    :rtype: String
    :return: The unquoted value extracted as an unicode
    string that the represents the same value.
    """

    value = legacy.unquote(value, *args, **kwargs)
    is_bytes = type(value) == legacy.BYTES
    if is_bytes: value = value.decode("utf-8")
    return value

def is_content_type(data, target):
    """
    Verifies if the any of the provided mime types (target) is
    valid for the provided content type string.

    :type data: String
    :param data: The content type string to be parsed and matched
    against the target mime type values.
    :type target: Tuple/String
    :param target: The tuple containing the multiple mime type values
    to be verified against the content type mime strings.
    :rtype: bool
    :return: If any of the provided mime types is considered valid
    for the content type.
    """

    if not isinstance(target, (list, tuple)): target = (target,)
    mime, _extra = parse_content_type(data)
    for item in target:
        type, _sub_type = item.split("/")
        wildcard = type + "/*"
        if item in mime: return True
        if wildcard in mime: return True
    return False

def parse_content_type(data):
    """
    Parses the provided content type string retrieving both the multiple
    mime types associated with the resource and the extra key to value
    items associated with the string in case they are defined (it's optional).

    :type data: String
    :param data: The content type data that is going to be parsed to
    obtain the structure of values for the content type string, this must
    be a plain unicode string and not a binary string.
    :rtype: Tuple
    :return: The sequence of mime types of the the content and the multiple
    extra values associated with the content type (eg: charset, boundary, etc.)
    """

    # creates the list of final normalized mime types and the
    # dictionary to store the extra values.
    types = []
    extra_m = dict()

    # in case no valid type has been sent returns the values
    # immediately to avoid further problems
    if not data: return types, extra_m

    # extracts the mime and the extra parts from the data string
    # they are the basis of the processing method
    data = data.strip(";")
    parts = data.split(";")
    mime = parts[0]
    extra = parts[1:]
    mime = mime.strip()

    # runs a series of verifications on the base mime value and in
    # case it's not valid returns the default values immediately
    if not "/" in mime: return types, extra_m

    # strips the complete set of valid extra values, note
    # that these values are going to be processed as key
    # to value items
    extra = [value.strip() for value in extra if extra]

    # splits the complete mime type into its type and sub
    # type components (first step of normalization)
    type, sub_type = mime.split("/", 1)
    sub_types = sub_type.split("+")

    # iterates over the complete set of sub types to
    # create the full mime type for each of them and
    # add the new full items to the types list (normalization)
    for sub_type in sub_types:
        types.append(type + "/" + sub_type)

    # goes through all of the extra key to value items
    # and converts them into proper dictionary values
    for extra_item in extra:
        if not "=" in extra_item: continue
        extra_item = extra_item.strip()
        key, value = extra_item.split("=")
        extra_m[key] = value

    # returns the final tuple containing both the normalized
    # mime types for the content and the extra key to value items
    return types, extra_m

def verify(condition, message = None, code = None, exception = None):
    if condition: return
    exception = exception or exceptions.AssertionError
    kwargs = dict()
    if not code == None: kwargs["code"] = code
    raise exception(
        message or "Assertion of data failed",
        **kwargs
    )

def execute(args, command = None, path = None, shell = True, encoding = None):
    if not encoding: encoding = sys.getfilesystemencoding()
    if command: args = command.split(" ")
    process = subprocess.Popen(
        args,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = shell,
        cwd = path
    )
    code = process.wait()
    stdout = process.stdout.read()
    stderr = process.stderr.read()
    stdout = stdout.decode(encoding)
    stderr = stderr.decode(encoding)
    return dict(
        stdout = stdout,
        stderr = stderr,
        code = code
    )

def _serialize(value):
    if value in legacy.STRINGS: return value
    return json.dumps(value)

class JSONEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        self.permissive = kwargs.pop("permissive", True)
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def default(self, obj, **kwargs):
        if hasattr(obj, "json_v"): return obj.json_v()
        if self.permissive: return str(obj)
        return json.JSONEncoder.default(self, obj, **kwargs)
