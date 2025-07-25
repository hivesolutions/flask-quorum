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

import quorum


class CryptTest(quorum.TestCase):

    @quorum.secured
    def test_rc4(self):
        rc4 = quorum.RC4(b"hello key")
        result = rc4.encrypt(b"hello world")

        self.assertEqual(result, b"\xc54L\x00\xac\xb4\xf2\xcf\x8b5\xa7")

        rc4 = quorum.RC4(b"hello key")
        data = rc4.decrypt(result)

        self.assertEqual(data, b"hello world")

        rc4 = quorum.Cipher.new("rc4", b"hello key")
        result = rc4.encrypt(b"hello world")

        self.assertEqual(result, b"\xc54L\x00\xac\xb4\xf2\xcf\x8b5\xa7")

        rc4 = quorum.Cipher.new("rc4", b"hello key")
        data = rc4.decrypt(result)

        self.assertEqual(data, b"hello world")

    @quorum.secured
    def test_spritz(self):
        spritz = quorum.Spritz(b"hello key")
        result = spritz.encrypt(b"hello world")

        self.assertEqual(result, b"\xbch\x0c\xb4X21\\\x07\xde\xe1")

        spritz = quorum.Spritz(b"hello key")
        data = spritz.decrypt(result)

        self.assertEqual(data, b"hello world")

        spritz = quorum.Cipher.new("spritz", b"hello key")
        result = spritz.encrypt(b"hello world")

        self.assertEqual(result, b"\xbch\x0c\xb4X21\\\x07\xde\xe1")

        spritz = quorum.Cipher.new("spritz", b"hello key")
        data = spritz.decrypt(result)

        self.assertEqual(data, b"hello world")
