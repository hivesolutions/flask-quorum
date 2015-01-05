#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import mock
import quorum

class ModelTest(quorum.TestCase):

    @quorum.secured
    def setUp(self):
        try:
            quorum.load(
                name = __name__,
                mongo_database = "test",
                models = mock
            )
            quorum.get_mongo()
        except:
            self.skip()

    @quorum.secured
    def tearDown(self):
        quorum.drop_mongo_db()
        quorum.unload()

    @quorum.secured
    def test_find(self):
        result = mock.Person.find(age = 1)
        self.assertEqual(len(result), 0)

        person = mock.Person()
        person.age = 1
        person.save()

        result = mock.Person.find(age = 1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].age, 1)

    @quorum.secured
    def test_count(self):
        result = mock.Person.count()
        self.assertEqual(result, 0)

        person = mock.Person()
        person.age = 1
        person.save()

        result = mock.Person.count()
        self.assertEqual(result, 1)
