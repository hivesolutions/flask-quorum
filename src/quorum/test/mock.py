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

import quorum

class Person(quorum.Model):

    identifier = quorum.field(
        type = int,
        index = True,
        increment = True,
        default = True
    )

    identifier_safe = quorum.field(
        type = int,
        index = True,
        increment = True,
        safe = True
    )

    name = quorum.field()

    age = quorum.field(
        type = int
    )

    father = quorum.field(
        type = quorum.reference(
            "Person",
            name = "identifier",
            dumpall = True
        )
    )

    brother = quorum.field(
        type = quorum.reference(
            "Person",
            name = "identifier"
        )
    )

    car = quorum.field(
        type = quorum.reference(
            "Car",
            name = "identifier"
        ),
        eager = True
    )

    cats = quorum.field(
        type = quorum.references(
            "Cat",
            name = "identifier"
        )
    )

    @classmethod
    def validate(cls):
        return super(Person, cls).validate() + [
            quorum.not_null("name"),
            quorum.not_empty("name"),
            quorum.not_duplicate("name", cls._name())
        ]

class Cat(quorum.Model):

    identifier = quorum.field(
        type = int,
        index = True,
        increment = True,
        default = True
    )

    identifier_safe = quorum.field(
        type = int,
        index = True,
        increment = True,
        safe = True
    )

    name = quorum.field()

class Car(quorum.Model):

    identifier = quorum.field(
        type = int,
        index = True,
        increment = True,
        default = True
    )

    identifier_safe = quorum.field(
        type = int,
        index = True,
        increment = True,
        safe = True
    )

    name = quorum.field()

    brand = quorum.field()

    variant = quorum.field()

    garage = quorum.field(
        type = quorum.reference(
            "Garage",
            name = "identifier"
        ),
        eager = True
    )

class Garage(quorum.Model):

    identifier = quorum.field(
        type = int,
        index = True,
        increment = True,
        default = True
    )

    identifier_safe = quorum.field(
        type = int,
        index = True,
        increment = True,
        safe = True
    )

    name = quorum.field()

    address = quorum.field(
        type = quorum.reference(
            "Address",
            name = "identifier"
        ),
        eager = True
    )

class Address(quorum.Model):

    identifier = quorum.field(
        type = int,
        index = True,
        increment = True,
        default = True
    )

    identifier_safe = quorum.field(
        type = int,
        index = True,
        increment = True,
        safe = True
    )

    street = quorum.field()
