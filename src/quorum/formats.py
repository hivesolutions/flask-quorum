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

from quorum import exceptions

try: import xlrd
except: xlrd = None

def xlsx_to_map(file_path, keys = (), ignore_header = True):
    # verifies if the xlrd module has been correctly loaded
    # and in case it's not raises an exception indicating so
    if xlrd == None: raise exceptions.ModuleNotFound("xlrd")

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
        if row == 0 and ignore_header: continue

        # creates the map that is going to be used in the construction
        # of the item elements and then iterates over all the expected
        # key values to populate it
        item = {}
        cell = 0
        for key in keys:
            cell_s = sheet.cell(row, cell)
            value = cell_s.value
            item[key] = value
            cell += 1

        # adds the item map that has been constructed to the list of
        # parsed items for the current spreadsheet
        items.append(item)

    # returns the final list of map items resulting from the parsing
    # of the spreadsheet file containing key to value assignments
    return items
