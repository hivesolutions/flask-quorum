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
import urllib
import urllib2

import exceptions

TIMEOUT = 10
""" The timeout in seconds to be used for the blocking
operations in the http connection """

def get_json(url, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _get_json(url, **kwargs)
        except urllib2.HTTPError, error:
            data = error.read()
            data_s = json.loads(data)
            raise exceptions.JsonError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def post_json(url, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _post_json(url, **kwargs)
        except urllib2.HTTPError, error:
            data = error.read()
            data_s = json.loads(data)
            raise exceptions.JsonError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def delete_json(url, **kwargs):
    # starts the variable holding the number of
    # retrieves to be used
    retries = 5

    while True:
        try:
            return _delete_json(url, **kwargs)
        except urllib2.HTTPError, error:
            data = error.read()
            data_s = json.loads(data)
            raise exceptions.JsonError(data_s)

        # decrements the number of retries and checks if the
        # number of retries has reached the limit
        retries -= 1
        if retries == 0:
            raise exceptions.HttpError("Data retrieval not possible")

def _get_json(url, **kwargs):
    values = kwargs or {}
    data = urllib.urlencode(values, doseq = True)
    url = url + "?" + data
    response = urllib2.urlopen(url, timeout = TIMEOUT)
    contents = response.read()
    contents_s = json.loads(contents) if contents else None
    return contents_s

def _post_json(url, **kwargs):
    values = kwargs or {}
    data = urllib.urlencode(values, doseq = True)
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request, timeout = TIMEOUT)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s

def _delete_json(url, **kwargs):
    values = kwargs or {}
    data = urllib.urlencode(values, doseq = True)
    url = url + "?" + data
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url)
    request.get_method = lambda: "DELETE"
    response = opener.open(request, timeout = TIMEOUT)
    contents = response.read()
    contents_s = json.loads(contents)
    return contents_s
