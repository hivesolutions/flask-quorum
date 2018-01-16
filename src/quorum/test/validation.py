#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import datetime

import quorum

class ValidationTest(quorum.TestCase):

    @quorum.secured
    def test_eq_number(self):
        methods = [quorum.eq("age", 2)]

        object = dict(age = 2)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2.0)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 3)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(age = "2")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(age = 2.01)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_eq_string(self):
        methods = [quorum.eq("name", "John Doe")]

        object = dict(name = "John Doe")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = "john doe")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(name = "JohnDoe")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(name = 2)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(name = 2.0)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(name = True)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_gt(self):
        methods = [quorum.gt("age", 2)]

        object = dict(age = 3)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2.01)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(age = "2")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        if quorum.legacy.PYTHON_3: self.assertFalse(result)
        else: self.assertTrue(result)

        object = dict(age = 1.99)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_gte(self):
        methods = [quorum.gte("age", 2)]

        object = dict(age = 3)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2.01)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2.00)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = "2")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        if quorum.legacy.PYTHON_3: self.assertFalse(result)
        else: self.assertTrue(result)

        object = dict(age = 1.99)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_lt(self):
        methods = [quorum.lt("age", 2)]

        object = dict(age = 1)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 1.99)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(age = "2")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(age = 2.01)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_lte(self):
        methods = [quorum.lte("age", 2)]

        object = dict(age = 1)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 1.99)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = 2.00)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(age = "2")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(age = 2.01)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_not_null(self):
        methods = [quorum.not_null("name")]

        object = dict(name = "John Doe")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = 1)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = 1.0)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = False)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = "")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = None)
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_not_empty(self):
        methods = [quorum.not_empty("name")]

        object = dict(name = "John Doe")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = [1, 2, 3])
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(name = "")
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

        object = dict(name = [])
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)

    @quorum.secured
    def test_not_past(self):
        methods = [quorum.not_past("time")]

        object = dict(time = datetime.datetime(2200, 1, 1))
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertTrue(result)

        object = dict(time = datetime.datetime(2001, 1, 1))
        result = quorum.validation.validate_b(
            methods = methods,
            object = object,
            build = False
        )
        self.assertFalse(result)
