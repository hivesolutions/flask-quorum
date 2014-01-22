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
import types
import flask
import string
import random
import thread
import defines

ALIAS = {
    "filter_def" : "find_d",
    "filter_string" : "find_s",
    "start_record" : "skip",
    "number_records" : "limit"
}
""" The map containing the various attribute alias
between the normalized manned and the quorum manner """

FIND_TYPES = {
    "skip" : int,
    "limit" : int,
    "find_s" : str,
    "find_d" : str
}
""" The map associating the various find fields with
their respective types """

def is_iterable(object):
    return type(object) in defines.ITERABLES

def request_json(request = None):
    # retrieves the proper request object, either the provided
    # request or the default flask request object and then in
    # case the the json data is already in the request properties
    # it is used (cached value) otherwise continues with the parse
    request = request or flask.request
    if "_data_j" in request.properties: return request.properties["_data_j"]

    # retrieves the current request data and tries to
    # "load" it as json data, in case it fails gracefully
    # handles the failure setting the value as an empty map
    data = request.data
    try: data_j = json.loads(data)
    except: data_j = {}
    request.properties["_data_j"] = data_j

    # returns the json data object to the caller method so that it
    # may be used as the parsed value (post information)
    return data_j

def get_field(name, default = None, cast = None):
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

    # in case the cast type value is set and the value is not invalid tries
    # to cast the value into the requested cast type
    if cast and not value == None: value = cast(value)

    # returns the final value to the caller method to be used, note that the
    # caller method should be aware of the sources used in the field retrieval
    return value

def get_object(object = None, alias = False, find = False, norm = True):
    # verifies if the provided object is valid in such case creates
    # a copy of it and uses it as the base object for validation
    # otherwise used an empty map (form validation)
    object = object and copy.copy(object) or {}

    # retrieves the current request data and tries to
    # "load" it as json data, in case it fails gracefully
    # handles the failure setting the value as an empty map
    data_j = request_json()

    # uses all the values referencing data in the request to try
    # to populate the object this way it may be constructed using
    # any of theses strategies (easier for the developer)
    for name, value in data_j.iteritems(): object[name] = value
    for name, value in flask.request.files.iteritems(): object[name] = value
    for name, value in flask.request.form_s.iteritems(): object[name] = value
    for name, value in flask.request.args_s.iteritems(): object[name] = value

    # in case the alias flag is set tries to resolve the attribute
    # alias and in case the find types are set converts the find
    # based attributes using the currently defined mapping map
    alias and resolve_alias(object)
    find and find_types(object)

    # in case the normalization flag is set runs the normalization
    # of the provided object so that sequences are properly handled
    # as define in the specification (this allows multiple references)
    norm and norm_object(object)

    # returns the constructed object to the caller method this object
    # should be a structured representation of the data in the request
    return object

def is_mobile():
    """
    Verifies if the current user agent string represents a
    mobile agent, for that a series of regular expressions
    are matched against the user agent string.

    @rtype: bool
    @return: If the current user agent string represents a
    mobile browser or a regular (desktop) one.
    """

    user_agent = flask.request.headers.get("User-Agent", "")
    prefix = user_agent[:4]
    mobile = defines.MOBILE_REGEX.search(user_agent)
    mobile_prefix = defines.MOBILE_PREFIX_REGEX.search(prefix)
    is_mobile = True if mobile or mobile_prefix else False
    return is_mobile

def resolve_alias(object):
    for name, value in object.items():
        if not name in ALIAS: continue
        _alias = ALIAS[name]
        object[_alias] = value
        del object[name]

def find_types(object):
    for name, value in object.items():
        if not name in FIND_TYPES:
            del object[name]
            continue
        find_type = FIND_TYPES[name]
        object[name] = find_type(value)

def norm_object(object):
    # iterates over all the key value association in the
    # object, trying to find the ones that refer sequences
    # so that they may be normalized
    for name, value in object.items():
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

        # retrieves the complete set of values for the current
        # iteration cycle and uses it to measure the number of
        # dictionary elements that are going to be contained in
        # the sequence to be "generated", then uses this (size)
        # value to pre-generate the complete set of dictionaries
        values = value.values()
        first = values[0] if values else None
        first_t = type(first)
        size = len(first) if first_t == types.ListType else 0
        if size == 0: list = [value]
        else: list = [dict() for _index in xrange(size)]

        # sets the list of generates dictionaries in the object for
        # the newly normalized name of structure
        object[name] = list

        # iterates over the complete set of key value pairs in the
        # value to gather the value into the various objects that
        # are contained in the sequence (normalization process)
        for key, value in value.items():
            for index in xrange(size):
                _object = list[index]
                _object[key] = value[index]

def load_form(form):
    # creates the map that is going to hold the "structured"
    # version of the form with key value associations
    form_s = {}

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
        value = value[0] if len(value) == 1 else value

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

def run_thread(function, *args, **kwargs):
    return thread.start_new_thread(function, args, kwargs)

def camel_to_underscore(camel):
    """
    Converts the provided camel cased based value into
    a normalized underscore based string.

    This is useful as most of the python string standards
    are compliant with the underscore strategy.

    @type camel: String
    @param camel: The camel cased string that is going to be
    converted into an underscore based string.
    @rtype: String
    @return The underscore based string resulting from the
    conversion of the provided camel cased one.
    """

    values = []
    camel_l = len(camel)

    for index in xrange(camel_l):
        char = camel[index]
        is_upper = char.isupper()

        if is_upper and not index == 0: values.append("_")
        values.append(char)

    return "".join(values).lower()

def generate_identifier(size = 16, chars = string.ascii_uppercase + string.digits):
    """
    Generates a random identifier (may be used as password) with
    the provided constrains of length and character ranges.

    This function may be used in the generation of random based
    keys for both passwords and api keys.

    @type size: int
    @param size: The size (in number of characters) to be used in
    the generation of the random identifier.
    @type chars: List
    @param chars: The list containing the characters to be used
    in the generation of the random identifier.
    @rtype: String
    @return: The randomly generated identifier obeying to the
    provided constrains.
    """

    return "".join(random.choice(chars) for _index in range(size))

def nl_to_br(value):
    """
    Replaces the occurrences of the newline character in the
    string with the html break line character.

    This is useful for one trying to convert a plain text
    representation of a string into html representation.

    @type value: String
    @param value: The base value that is going to be used in
    the conversion to the html value.
    @rtype: String
    @return: The string containing the newline characters replaced
    with line breaking html tags.
    """

    return value.replace("\n", "<br/>\n")
