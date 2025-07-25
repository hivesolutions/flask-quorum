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

import json

import quorum


class ExportTest(quorum.TestCase):

    def setUp(self):
        try:
            quorum.load(name=__name__)
        except Exception:
            self.skip()

    def tearDown(self):
        try:
            adapter = quorum.get_adapter()
            adapter.drop_db()
        except Exception:
            pass
        finally:
            quorum.unload()

    @quorum.secured
    def test_import_single(self):
        structure = {
            "person:id": dict(_id="person:id", seq=11),
            "account:id": dict(_id="account:id", seq=33),
        }
        data = json.dumps(structure)
        data = quorum.legacy.bytes(data)

        adapter = quorum.get_adapter()
        manager = quorum.export.ExportManager(adapter, multiple=quorum.resolve())

        collection = adapter.collection("counter")
        manager._import_single(collection, data, key="_id")

        values = collection.find()
        values = [value for value in values]

        self.assertEqual(type(values), list)
        self.assertEqual(len(values), 2)

        value = collection.find_one(dict(_id="person:id"))

        self.assertEqual(value["seq"], 11)

    @quorum.secured
    def test_import_multiple(self):
        data = [
            (
                "person:id",
                quorum.legacy.bytes(
                    json.dumps(dict(_id="person:id", seq=11)), encoding="utf-8"
                ),
            ),
            (
                "account:id",
                quorum.legacy.bytes(
                    json.dumps(dict(_id="account:id", seq=33)), encoding="utf-8"
                ),
            ),
        ]

        adapter = quorum.get_adapter()
        manager = quorum.export.ExportManager(adapter, multiple=quorum.resolve())

        collection = adapter.collection("counter")
        manager._import_multiple(collection, data, key="_id")

        values = collection.find()
        values = [value for value in values]

        self.assertEqual(type(values), list)
        self.assertEqual(len(values), 2)

        value = collection.find_one(dict(_id="person:id"))

        self.assertEqual(value["seq"], 11)
