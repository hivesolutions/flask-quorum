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

import quorum

class BaseTest(quorum.TestCase):

    def setUp(self):
        try:
            quorum.load(name = __name__)
        except:
            self.skip()

    def tearDown(self):
        quorum.unload()

    @quorum.secured
    def test_locale(self):
        app = quorum.get_app()
        app.locales = ("en_us", "pt_pt", "es_es")
        app.bundles["en_us"] = dict(hello = "Hello")
        app.bundles["pt_pt"] = dict(hello = "Olá")

        result = quorum.to_locale("hello", locale = "en-us")
        self.assertEqual(result, "Hello")

        result = quorum.to_locale("hello", locale = "pt_pt")
        self.assertEqual(result, "Olá")

        result = quorum.to_locale("hello", locale = "pt-pt")
        self.assertNotEqual(result, "Olá")
        self.assertEqual(result, "Hello")

        result = quorum.to_locale("hello", locale = "es_es")
        self.assertNotEqual(result, "Hola")
        self.assertEqual(result, "Hello")

        app.bundles["es_es"] = dict(hello = "Hola")

        result = quorum.to_locale("hello", locale = "es_es")
        self.assertEqual(result, "Hola")

        result = quorum.to_locale("hello", locale = "en")
        self.assertEqual(result, "Hello")

        result = quorum.to_locale("hello", locale = "pt")
        self.assertEqual(result, "Olá")

        result = quorum.to_locale("hello", locale = "es")
        self.assertEqual(result, "Hola")

        result = quorum.to_locale("bye", locale = "en_us")
        self.assertEqual(result, "bye")

        result = quorum.to_locale("bye", locale = "cn")
        self.assertEqual(result, "bye")

        app.bundles["en_us"].update(bye = "Bye")

        result = quorum.to_locale("bye", locale = "en_us")
        self.assertEqual(result, "Bye")

        result = quorum.to_locale("bye", locale = "pt_pt")
        self.assertEqual(result, "Bye")

        result = quorum.to_locale("bye", locale = "pt_pt", fallback = False)
        self.assertEqual(result, "bye")
