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

from . import mock

class TypesfTest(quorum.TestCase):

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

    @quorum.secured
    def test_reference(self):
        person = mock.Person()
        person.name = "Name"
        person.car = mock.Person.car["type"]("")

        self.assertEqual(person.car, None)
        self.assertEqual(person.car, mock.Person.car["type"](""))
        self.assertEqual(person.car, mock.Person.car["type"](b""))
        self.assertEqual(person.car, mock.Person.car["type"](None))
        self.assertNotEqual(person.car, mock.Person.father["type"](1))
        self.assertNotEqual(person.car, mock.Person.car["type"](1))
        self.assertNotEqual(person.car, "car")
        self.assertEqual(isinstance(person.car, quorum.Reference), True)
        self.assertEqual(len(person.car), 0)

        person = mock.Person()
        person.name = "Name"
        person.car = mock.Person.car["type"](b"")

        self.assertEqual(person.car, None)
        self.assertEqual(person.car, mock.Person.car["type"](""))
        self.assertEqual(person.car, mock.Person.car["type"](b""))
        self.assertEqual(person.car, mock.Person.car["type"](None))
        self.assertNotEqual(person.car, mock.Person.father["type"](1))
        self.assertNotEqual(person.car, mock.Person.car["type"](1))
        self.assertNotEqual(person.car, "car")
        self.assertEqual(isinstance(person.car, quorum.Reference), True)
        self.assertEqual(len(person.car), 0)

        person = mock.Person()
        person.name = "Name"
        person.car = mock.Person.car["type"](None)

        self.assertEqual(person.car, None)
        self.assertEqual(person.car, mock.Person.car["type"](""))
        self.assertEqual(person.car, mock.Person.car["type"](b""))
        self.assertEqual(person.car, mock.Person.car["type"](None))
        self.assertNotEqual(person.car, mock.Person.father["type"](1))
        self.assertNotEqual(person.car, mock.Person.car["type"](1))
        self.assertNotEqual(person.car, "car")
        self.assertEqual(isinstance(person.car, quorum.Reference), True)
        self.assertEqual(len(person.car), 0)

        person = mock.Person()
        person.name = "Name"
        person.car = mock.Person.car["type"](1)

        self.assertEqual(person.car, mock.Person.car["type"](1))
        self.assertNotEqual(person.car, None)
        self.assertNotEqual(person.car, mock.Person.car["type"](""))
        self.assertNotEqual(person.car, mock.Person.car["type"](b""))
        self.assertNotEqual(person.car, mock.Person.car["type"](None))
        self.assertNotEqual(person.car, mock.Person.father["type"](1))
        self.assertNotEqual(person.car, "car")
        self.assertEqual(isinstance(person.car, quorum.Reference), True)
        self.assertEqual(len(person.car), 1)

    @quorum.secured
    def test_references(self):
        person = mock.Person()
        person.name = "Name"
        person.cats = mock.Person.cats["type"]([1, 2, 3])

        self.assertEqual(mock.Cat(identifier = 1) in person.cats, True)
        self.assertEqual(mock.Cat(identifier = 3) in person.cats, True)
        self.assertNotEqual(mock.Cat(identifier = 4) in person.cats, True)
        self.assertNotEqual(person.cats, None)
        self.assertNotEqual(person.cats, [])
        self.assertNotEqual(person.cats, "cars")
        self.assertEqual(isinstance(person.cats, quorum.References), True)
        self.assertEqual(len(person.cats), 3)

    @quorum.secured
    def test_file(self):
        file_m = dict(name = "hello", data = b"SGVsbG8gV29ybGQ=")
        file = quorum.File(file_m)

        self.assertEqual(type(file.file_name), str)
        self.assertEqual(type(file.data_b64), str)
        self.assertEqual(type(file.data), quorum.legacy.BYTES)
        self.assertEqual(file.file_name, "hello")
        self.assertEqual(file.data, b"Hello World")
        self.assertEqual(file.data_b64, "SGVsbG8gV29ybGQ=")

        file_d = b"Hello World"
        file = quorum.File(file_d)

        self.assertEqual(type(file.file_name), str)
        self.assertEqual(type(file.data_b64), str)
        self.assertEqual(type(file.data), quorum.legacy.BYTES)
        self.assertEqual(file.file_name, "default")
        self.assertEqual(file.data, b"Hello World")
        self.assertEqual(file.data_b64, "SGVsbG8gV29ybGQ=")

    @quorum.secured
    def test_encrypted(self):
        encrypted = quorum.encrypted(key = b"hello key")
        result = encrypted("hello world")

        self.assertEqual(str(result), "hello world")
        self.assertEqual(result.value, "hello world")
        self.assertEqual(result.encrypted, "vGgMtFgyMVwH3uE=:encrypted")

        result = encrypted("vGgMtFgyMVwH3uE=:encrypted")

        self.assertEqual(str(result), "hello world")
        self.assertEqual(result.value, "hello world")
        self.assertEqual(result.encrypted, "vGgMtFgyMVwH3uE=:encrypted")

        encrypted = quorum.encrypted(key = None)
        result = encrypted("hello world")

        self.assertEqual(str(result), "hello world")
        self.assertEqual(result.value, "hello world")
        self.assertEqual(result.value, "hello world")

        result = encrypted("vGgMtFgyMVwH3uE=:encrypted")

        self.assertEqual(str(result), "vGgMtFgyMVwH3uE=:encrypted")
        self.assertEqual(result.value, "vGgMtFgyMVwH3uE=:encrypted")
        self.assertEqual(result.encrypted, "vGgMtFgyMVwH3uE=:encrypted")

    @quorum.secured
    def test_dumpall(self):
        person = mock.Person()
        person.name = "Name"
        person.save()

        car = mock.Car()
        car.name = "Car"
        car.save()

        father = mock.Person()
        father.name = "Father"
        father.save()

        brother = mock.Person()
        brother.name = "Brother"
        brother.save()

        person.car = car
        person.father = father
        person.brother = brother
        person.save()

        person = mock.Person.get(identifier = 1)

        result = person.json_v()

        self.assertEqual(type(result), dict)
        self.assertEqual(result["name"], "Name")

        result = person.car.json_v()

        self.assertEqual(type(result), int)
        self.assertEqual(result, 1)

        result = person.father.json_v()

        self.assertEqual(type(result), mock.Person)
        self.assertEqual(result.name, "Father")

        result = person.brother.json_v()

        self.assertEqual(type(result), int)
        self.assertEqual(result, 3)
