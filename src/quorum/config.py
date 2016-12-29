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

import os
import sys
import json

from . import legacy

FILE_NAME = "quorum.json"
""" The default name of the file that is going to be
used for the loading of configuration values from json """

FILE_TEMPLATE = "quorum.%s.json"
""" The template to be used in the construction of the
domain specific configuration file paths """

HOME_FILE = "~/.home"
""" The location of the file that may be used to "redirect"
the home directory contents to a different directory """

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
be used to try to decode possible byte based strings
for the various environment variable values """

config_g = {}
""" The map containing the various global wide
configuration for the current application """

config_f = []
""" The list of files that have been used for the loading
of the configuration through this session, every time a
loading of configuration from a file occurs the same path
is added to this global list """

homes = []
""" Global reference to the paths to the directory considered
to be the home on in terms of configuration, this value should
be set on the initial loading of the ".home" file """

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

def conf_suffix(suffix):
    config = dict()
    for name, value in config_g.items():
        if not name.endswith(suffix): continue
        config[name] = value
    return config

def confs(name, value):
    global config_g
    config_g[name] = value

def confd():
    return config_g

def load(names = (FILE_NAME,), path = None, encoding = "utf-8"):
    paths = []
    homes = get_homes()
    for home in homes:
        paths += [
            os.path.join(home),
            os.path.join(home, ".config"),
        ]
    paths += [sys.prefix]
    paths.append(path)
    for path in paths:
        for name in names:
            load_file(name = name, path = path, encoding = encoding)
    load_env()

def load_file(name = FILE_NAME, path = None, encoding = "utf-8"):
    if path: path = os.path.normpath(path)
    if path: file_path = os.path.join(path, name)
    else: file_path = name

    file_path = os.path.abspath(file_path)
    file_path = os.path.normpath(file_path)

    exists = os.path.exists(file_path)
    if not exists: return

    exists = file_path in config_f
    if exists: config_f.remove(file_path)
    config_f.append(file_path)

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

def get_homes(
    file_path = HOME_FILE,
    default = "~",
    encoding = "utf-8",
    force_default = False
):
    global homes
    if homes: return homes

    homes = os.environ.get("HOMES", None)
    homes = homes.split(";") if homes else homes
    if not homes == None: return homes

    default = os.path.expanduser(default)
    default = os.path.abspath(default)
    default = os.path.normpath(default)
    homes = [default]

    file_path = os.path.expanduser(file_path)
    file_path = os.path.normpath(file_path)
    exists = os.path.exists(file_path)
    if not exists: return homes

    if not force_default: del homes[:]

    file = open(file_path, "rb")
    try: data = file.read()
    finally: file.close()

    data = data.decode("utf-8")
    data = data.strip()
    paths = data.split()

    for path in paths:
        path = path.strip()
        if not path: continue
        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        path = os.path.normpath(path)
        homes.append(path)

    return homes

load()
