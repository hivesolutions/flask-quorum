#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2022 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2022 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import quorum


class FormatsTest(quorum.TestCase):

    def setUp(self):
        # stores the original xlrd reference so it can be
        # restored after each test execution
        self._original_xlrd = quorum.formats.xlrd

        # replaces the xlrd module reference in formats with
        # our mock implementation for testing purposes
        quorum.formats.xlrd = MockXlrd()

    def tearDown(self):
        # restores the original xlrd reference after each test
        # to prevent side effects between tests
        quorum.formats.xlrd = self._original_xlrd

    @quorum.secured
    def test_xlsx_raw_text_cell(self):
        # creates a mock cell with text type and verifies
        # that the value is returned directly without conversion
        cell = MockCell(MockXlrd.XL_CELL_TEXT, "Hello World")
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, quorum.legacy.u("Hello World"))
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_text_cell_unicode(self):
        # creates a mock cell with text type containing unicode
        # characters and verifies proper handling
        cell = MockCell(MockXlrd.XL_CELL_TEXT, "Olá Mundo")
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, quorum.legacy.u("Olá Mundo"))
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_text_cell_empty(self):
        # creates a mock cell with text type and empty quorum.legacy.UNICODEing
        # value to verify edge case handling
        cell = MockCell(MockXlrd.XL_CELL_TEXT, "")
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "")
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_integer_value(self):
        # creates a mock cell with a numeric type that contains
        # an integer value; the modulo check detects whole numbers
        # and returns them without decimal places
        cell = MockCell(MockXlrd.XL_CELL_NUMBER, 42.0)
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "42")
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_integer_value_zero(self):
        # creates a mock cell with zero integer value to verify
        # proper handling of zero values
        cell = MockCell(MockXlrd.XL_CELL_NUMBER, 0.0)
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "0")
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_integer_value_negative(self):
        # creates a mock cell with a negative integer value to
        # verify proper handling of negative numbers
        cell = MockCell(MockXlrd.XL_CELL_NUMBER, -100.0)
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "-100")
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_float_value(self):
        # creates a mock cell with a numeric type that contains
        # a float value with decimal places
        cell = MockCell(MockXlrd.XL_CELL_NUMBER, 3.14159)
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "3.14159")
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_float_value_negative(self):
        # creates a mock cell with a negative float value to
        # verify proper handling of negative decimals
        cell = MockCell(MockXlrd.XL_CELL_NUMBER, -2.5)
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "-2.5")
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_large_integer(self):
        # creates a mock cell with a large integer value to
        # verify proper handling without scientific notation issues
        cell = MockCell(MockXlrd.XL_CELL_NUMBER, 123456789.0)
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "123456789")
        self.assertEqual(type(result), quorum.legacy.UNICODE)

    @quorum.secured
    def test_xlsx_raw_small_float(self):
        # creates a mock cell with a very small float value to
        # verify proper precision handling
        cell = MockCell(MockXlrd.XL_CELL_NUMBER, 0.001)
        result = quorum.formats.xlsx_raw(cell)

        self.assertEqual(result, "0.001")
        self.assertEqual(type(result), quorum.legacy.UNICODE)


class MockXlrd:
    """
    Mock class that simulates the xlrd module constants
    used for cell type identification.
    """

    XL_CELL_TEXT = 1
    XL_CELL_NUMBER = 2


class MockCell:
    """
    Mock class that simulates an xlrd cell object with
    ctype and value attributes for testing purposes.
    """

    def __init__(self, ctype, value):
        self.ctype = ctype
        self.value = value
