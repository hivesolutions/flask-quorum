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

import string

import quorum

class UtilTest(quorum.TestCase):

    def setUp(self):
        try:
            quorum.load(name = __name__)
        except:
            self.skip()

    def tearDown(self):
        quorum.unload()

    @quorum.secured
    def test_camel_to_underscore(self):
        result = quorum.camel_to_underscore("HelloWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "hello_world")

        result = quorum.camel_to_underscore("HELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "hello_world")

        result = quorum.camel_to_underscore("HELLOWorldHELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "hello_world_hello_world")

    @quorum.secured
    def test_camel_to_readable(self):
        result = quorum.camel_to_readable("HelloWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.camel_to_readable("HelloWorld", lower = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world")

        result = quorum.camel_to_readable("HelloWorld", lower = True, capitalize = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.camel_to_readable("HELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "HELLO World")

        result = quorum.camel_to_readable("HELLOWorld", lower = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world")

        result = quorum.camel_to_readable(
            "HELLOWorld",
            lower = True,
            capitalize = True
        )
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.camel_to_readable("HELLOWorldHELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "HELLO World HELLO World")

        result = quorum.camel_to_readable(
            "HELLOWorldHELLOWorld",
            lower = True
        )
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world hello world")

        result = quorum.camel_to_readable(
            "HELLOWorldHELLOWorld",
            lower = True,
            capitalize = True
        )
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World Hello World")

    @quorum.secured
    def test_underscore_to_readable(self):
        result = quorum.underscore_to_readable("hello_world")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world")

        result = quorum.underscore_to_readable("hello_world", capitalize = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.underscore_to_readable("hello_world_hello_world")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world hello world")

        result = quorum.underscore_to_readable("hello_world_hello_world", capitalize = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World Hello World")

    @quorum.secured
    def test_generate_identifier(self):
        identifier = quorum.generate_identifier(
            size = 16,
            chars = string.ascii_uppercase
        )
        self.assertEqual(len(identifier), 16)
        for char in identifier:
            self.assertTrue(char in string.ascii_uppercase)

    @quorum.secured
    def test_is_content_type(self):
        result = quorum.is_content_type("text/plain", "text/plain")
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/plain", ("text/plain",))
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/plain", "text/html")
        self.assertEqual(result, False)

        result = quorum.is_content_type("text/plain", ("text/html",))
        self.assertEqual(result, False)

        result = quorum.is_content_type("text/plain", ("text/plain", "text/html"))
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/*", "text/plain")
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/*", "text/json")
        self.assertEqual(result, True)

    @quorum.secured
    def test_parse_content_type(self):
        result = quorum.parse_content_type("text/plain")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain"])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text/plain+json")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text/plain+json; charset=utf-8")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict(charset = "utf-8"))

        result = quorum.parse_content_type("text/plain+json   ; charset=utf-8")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict(charset = "utf-8"))

        result = quorum.parse_content_type("text/plain+json; charset=utf-8; boundary=hello;")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict(charset = "utf-8", boundary = "hello"))

        result = quorum.parse_content_type("")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text/plain+json; charset")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict())
