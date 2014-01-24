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

import os
import sys
import setuptools

BASE_PATH = os.path.realpath(__file__)
BASE_DIR = os.path.dirname(BASE_PATH)
QUORUM_DIR = os.path.join(BASE_DIR, "src", "quorum")
sys.path.insert(0, QUORUM_DIR)

import info

setuptools.setup(
    name = info.NAME,
    version = info.VERSION,
    author = info.AUTHOR,
    author_email = info.EMAIL,
    description = info.DESCRIPTION,
    license = info.LICENSE,
    keywords = info.KEYWORDS,
    url = info.URL,
    zip_safe = True,
    packages = [
        "quorum",
        "quorum.test"
    ],
    test_suite = "quorum.test",
    package_dir = {
        "" : os.path.normpath("src")
    },
    install_requires = [
        "flask"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ]
)
