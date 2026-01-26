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

from . import legacy
from . import exceptions

try:
    import xlrd
except ImportError:
    xlrd = None


def xlsx_to_map(file_path, keys=(), types=(), ignore_header=True):
    """
    Parses an Excel spreadsheet (.xlsx or .xls) file and converts its contents
    into a list of dictionaries (maps), where each row becomes a dictionary entry.
    This function is particularly useful for importing structured data from Excel
    files into Python applications, enabling seamless integration with business
    workflows that rely on spreadsheet-based data exchange.

    The function uses the xlrd library to read the workbook and processes only
    the first sheet. Each row in the sheet is mapped to a dictionary using the
    provided keys sequence, where each key corresponds to a column in order.

    Optional type conversion can be applied to each column via the types parameter,
    allowing automatic casting of cell values (e.g., int, float, str).

    :type file_path: String
    :param file_path: The absolute or relative file path to the Excel spreadsheet
    file that should be parsed and converted into a list of dictionaries.
    :type keys: Tuple
    :param keys: A sequence of strings representing the dictionary keys to use
    for each column. The order must match the column order in the spreadsheet.
    :type types: Tuple
    :param types: A sequence of callable types (e.g., int, float, str) for
    converting each column's raw value. Use None for columns that need no conversion.
    :type ignore_header: bool
    :param ignore_header: If True (default), the first row of the spreadsheet
    is skipped, assuming it contains column headers rather than data.
    :rtype: List
    :return: A list of dictionaries where each dictionary represents a row
    from the spreadsheet with keys mapped to their corresponding cell values.
    """

    # verifies if the xlrd module has been correctly loaded
    # and in case it's not raises an exception indicating so
    if xlrd == None:
        raise exceptions.ModuleNotFound("xlrd")

    # in case the (data types) sequence is not defined creates
    # a tuple of unset types to fill the values
    if not types:
        types = tuple([None] * len(keys))

    # creates the list structure that is going to store the
    # complete set of parsed items according to the provided
    # keys list specification
    items = []

    # opens the workbook in the provided file path for reading
    # of its contents and construction of the final structure
    workbook = xlrd.open_workbook(file_path)

    # retrieves the list of sheets in the document and retrieves
    # the first of its sheets, this the one that is going to be
    # used in the processing of the contents (considered primary)
    sheets = workbook.sheets()
    sheet = sheets[0]

    # iterates over the complete set of valid rows in the sheet
    # to process its contents, the valid rows are the ones that
    # contain any sort of data
    for row in range(sheet.nrows):
        # in case the ignore header flag is set and the current
        # row index is zero must continue the loop ignoring it
        if row == 0 and ignore_header:
            continue

        # creates the map that is going to be used in the construction
        # of the item elements and then iterates over all the expected
        # key values to populate it
        item = {}
        cell = 0
        for key, type in zip(keys, types):
            cell_s = sheet.cell(row, cell)
            raw = xlsx_raw(cell_s)
            value = cell_s.value
            if type:
                value = type(raw)
            item[key] = value
            cell += 1

        # adds the item map that has been constructed to the list of
        # parsed items for the current spreadsheet
        items.append(item)

    # returns the final list of map items resulting from the parsing
    # of the spreadsheet file containing key to value assignments
    return items


def xlsx_raw(cell_s):
    """
    Sanitizes the string value for the cell, taking into
    consideration integers and strings as different data types,
    the returning value is always a string.

    :type cell_s: Cell
    :param cell_S: The cell base value, that is going to be
    tested for data type and from which a sanitized string
    value should be returned.
    :rtype: String
    :return: The sanitized string value from the cell value
    ready to be used.
    """

    # in case the cell is a text cell returns the value
    # directly without any conversion or processing
    is_str = cell_s.ctype == xlrd.XL_CELL_TEXT
    if is_str:
        return legacy.u(cell_s.value, force=True)

    # uses modulo to check if value has no fractional part
    # returning as integer string if so, otherwise as float
    # in case of an error returns the value as a string, this
    # is a fallback coercion strategy to handle unexpected cases
    try:
        if float(cell_s.value) % 1 == 0:
            return legacy.UNICODE(int(cell_s.value))
        return legacy.UNICODE(float(cell_s.value))
    except (ValueError, TypeError):
        return legacy.UNICODE(cell_s.value)
