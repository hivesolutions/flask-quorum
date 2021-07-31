#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2021 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2021 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys
import json

from . import legacy

FILE_NAME = "quorum.json"
""" The default name of the file that is going to be
used for the loading of configuration values from JSON """

FILE_TEMPLATE = "quorum.%s.json"
""" The template to be used in the construction of the
domain specific configuration file paths """

HOME_FILE = "~/.home"
""" The location of the file that may be used to "redirect"
the home directory contents to a different directory """

IMPORT_NAMES = ("$import", "$include", "$IMPORT", "$INCLUDE")
""" The multiple possible definitions of the special configuration
name that references a list of include files to be loaded """

CASTS = {
    bool : lambda v: v if isinstance(v, bool) else v in ("1", "true", "True"),
    list : lambda v: v if isinstance(v, list) else v.split(";") if v else [],
    tuple : lambda v: v if isinstance(v, tuple) else tuple(v.split(";") if v else [])
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

if not isinstance(__builtins__, dict):
    __builtins__ = __builtins__.__dict__

def conf(name, default = None, cast = None, ctx = None):
    config = ctx["config"] if ctx else config_g
    cast = _cast_r(cast)
    value = config.get(name, default)
    if cast and not value == None: value = cast(value)
    return value

def conf_prefix(prefix, ctx = None):
    config = ctx["config"] if ctx else config_g
    config_prefix = dict()
    for name, value in config.items():
        if not name.startswith(prefix): continue
        config_prefix[name] = value
    return config_prefix

def conf_suffix(suffix, ctx = None):
    config = ctx["config"] if ctx else config_g
    config_suffix = dict()
    for name, value in config.items():
        if not name.endswith(suffix): continue
        config_suffix[name] = value
    return config_suffix

def confs(name, value, ctx = None):
    config = ctx["config"] if ctx else config_g
    config[name] = value

def confr(name, ctx = None):
    config = ctx["config"] if ctx else config_g
    if not name in config: return
    del config[name]

def confd(ctx = None):
    config = ctx["config"] if ctx else config_g
    return config

def confctx():
    return dict(config = dict(), config_f = dict())

def load(names = (FILE_NAME,), path = None, encoding = "utf-8", ctx = None):
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
            load_file(name = name, path = path, encoding = encoding, ctx = ctx)
    load_env(ctx = ctx)

def load_file(name = FILE_NAME, path = None, encoding = "utf-8", ctx = None):
    config = ctx["config"] if ctx else config_g
    _config_f = ctx["config_f"] if ctx else config_f

    if path: path = os.path.normpath(path)
    if path: file_path = os.path.join(path, name)
    else: file_path = name

    file_path = os.path.abspath(file_path)
    file_path = os.path.normpath(file_path)
    base_path = os.path.dirname(file_path)

    exists = os.path.exists(file_path)
    if not exists: return

    exists = file_path in _config_f
    if exists: _config_f.remove(file_path)
    _config_f.append(file_path)

    file = open(file_path, "rb")
    try: data = file.read()
    finally: file.close()
    if not data: return

    data = data.decode(encoding)
    data_j = json.loads(data)

    _load_includes(base_path, data_j, encoding = encoding)

    for key, value in data_j.items():
        if not _is_valid(key): continue
        config[key] = value

def load_env(ctx = None):
    _config = ctx["config"] if ctx else config_g

    config = dict(os.environ)
    homes = get_homes()

    for home in homes:
        _load_includes(home, config)

    for key, value in legacy.iteritems(config):
        if not _is_valid(key): continue
        _config[key] = value
        is_bytes = legacy.is_bytes(value)
        if not is_bytes: continue
        for encoding in ENV_ENCODINGS:
            try: value = value.decode(encoding)
            except UnicodeDecodeError: pass
            else: break
        _config[key] = value

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
    paths = data.splitlines()
    paths = [path.strip() for path in paths]

    for path in paths:
        path = path.strip()
        if not path: continue
        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        path = os.path.normpath(path)
        homes.append(path)

    return homes

def _cast_r(cast):
    is_string = type(cast) in legacy.STRINGS
    if is_string: cast = __builtins__.get(cast, None)
    if not cast: return None
    return CASTS.get(cast, cast)

def _load_includes(base_path, config, encoding = "utf-8"):
    includes = ()

    for alias in IMPORT_NAMES:
        includes = config.get(alias, includes)

    if legacy.is_string(includes):
        includes = includes.split(";")

    for include in includes:
        load_file(
            name = include,
            path = base_path,
            encoding = encoding
        )

def _is_valid(key):
    if key in IMPORT_NAMES: return False
    return True

load()
