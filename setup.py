#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2025 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2025 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import sys
import setuptools

BASE_PATH = os.path.realpath(__file__)
BASE_DIR = os.path.dirname(BASE_PATH)
SRC_DIR = os.path.join(BASE_DIR, "src")
QUORUM_DIR = os.path.join(SRC_DIR, "quorum")
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, QUORUM_DIR)

import info

setuptools.setup(
    name=info.NAME,
    version=info.VERSION,
    author=info.AUTHOR,
    author_email=info.EMAIL,
    description=info.DESCRIPTION,
    license=info.LICENSE,
    keywords=info.KEYWORDS,
    url=info.URL,
    zip_safe=True,
    packages=["quorum", "quorum.test"],
    test_suite="quorum.test",
    package_dir={"": os.path.normpath("src")},
    install_requires=["flask"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md"), "rb")
    .read()
    .decode("utf-8"),
    long_description_content_type="text/markdown",
)
