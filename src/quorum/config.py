#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys
import json

from . import legacy

FILE_NAME = "quorum.json"
""" The default name of the file that is going to be
used for the loading of configuration values from json """

CASTS = {
    bool : lambda v: v if type(v) == bool else v == "1",
    list : lambda v: v if type(v) == list else v.split(";"),
    tuple : lambda v: v if type(v) == tuple else tuple(v.split(";"))
}
""" The map containing the various cast method
operation associated with the various data types,
they provide a different type of casting strategy """

ENV_ENCODINGS = (
    "utf-8",
    sys.getdefaultencoding(),
    sys.getfilesystemencoding()
)
""" The sequence of encodings that are going to
be ued to try to decode possible byte based strings
for the various environment variable values """

config_g = {}
""" The map containing the various global wide
configuration for the current application """

def conf(name, default = None, cast = None):
    is_string = type(cast) in legacy.STRINGS
    if is_string: cast = __builtins__.get(cast, None)
    cast = CASTS.get(cast, cast)
    value = config_g.get(name, default)
    value = cast(value) if cast else value
    return value

def conf_prefix(prefix):
    config = dict()
    for name, value in config_g.items():
        if not name.startswith(prefix): continue
        config[name] = value
    return config

def confs(name, value):
    global config_g
    config_g[name] = value

def load(path = None):
    load_file(path = os.path.expanduser("~"))
    load_file(path = sys.prefix)
    load_file(path = path)
    load_env()

def load_file(path = None, encoding = "utf-8"):
    if path: file_path = os.path.join(path, FILE_NAME)
    else: file_path = FILE_NAME

    exists = os.path.exists(file_path)
    if not exists: return

    file = open(file_path, "rb")
    try: data = file.read()
    finally: file.close()
    if not data: return

    data = data.decode(encoding)
    data_j = json.loads(data)
    for key, value in data_j.items():
        config_g[key] = value

def load_env():
    for key, value in os.environ.items():
        config_g[key] = value
        is_bytes = legacy.is_bytes(value)
        if not is_bytes: continue
        for encoding in ENV_ENCODINGS:
            try: value = value.decode(encoding)
            except UnicodeDecodeError: pass
            else: break
        config_g[key] = value

load()
