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

import unittest

import quorum

from . import mock

class ModelTest(unittest.TestCase):

    def setUp(self):
        try:
            quorum.load(
                name = __name__,
                mongo_database = "test",
                models = mock
            )
        except:
            self.skip()

    def tearDown(self):
        try:
            adapter = quorum.get_adapter()
            adapter.drop_db()
        except: pass
        finally: quorum.unload()

    def test_reference(self):
        person = mock.Person()
        person.name = "Name"
        person.car = mock.Person.car["type"]("")

        self.assertEqual(person.car, None)
        self.assertEqual(isinstance(person.car, quorum.Reference), True)
        self.assertEqual(len(person.car), 0)

        person = mock.Person()
        person.name = "Name"
        person.car = mock.Person.car["type"](b"")

        self.assertEqual(person.car, None)
        self.assertEqual(isinstance(person.car, quorum.Reference), True)
        self.assertEqual(len(person.car), 0)

        person = mock.Person()
        person.name = "Name"
        person.car = mock.Person.car["type"](None)

        self.assertEqual(person.car, None)
        self.assertEqual(isinstance(person.car, quorum.Reference), True)
        self.assertEqual(len(person.car), 0)
