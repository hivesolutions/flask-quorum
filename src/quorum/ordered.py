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

class Ordered(type):
    """
    Metaclass to be used for classes where the
    definition order of its attributes is critical
    for the correct process.
    """

    def __new__(cls, name, bases, attrs):
        new_cls = super(Ordered, cls).__new__(cls, name, bases, attrs)
        new_cls._ordered = [(name, attrs.pop(name)) for name, value in attrs.items()\
            if hasattr(value, "creation_counter")]
        new_cls._ordered.sort(key = lambda item: item[1].creation_counter)
        new_cls._ordered = [name for name, value in new_cls._ordered]
        return new_cls

    def __init__(cls, name, bases, attrs):
        super(Ordered, cls).__init__(name, bases, attrs)
