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

import quorum


class MongoDbTest(quorum.TestCase):

    def test__parse_uri(self):
        result = quorum.mongodb._parse_uri("mongodb://localhost")
        self.assertEqual(result["nodelist"], [("localhost", 27017)])
        self.assertEqual(result["username"], None)
        self.assertEqual(result["password"], None)
        self.assertEqual(result["database"], None)
        self.assertEqual(result["options"], {})

        result = quorum.mongodb._parse_uri("mongodb://admin:pass@localhost/main")
        self.assertEqual(result["nodelist"], [("localhost", 27017)])
        self.assertEqual(result["username"], "admin")
        self.assertEqual(result["password"], "pass")
        self.assertEqual(result["database"], "main")
        self.assertEqual(result["options"], {})

        result = quorum.mongodb._parse_uri("mongodb://admin:pass@localhost:27017/main")
        self.assertEqual(result["nodelist"], [("localhost", 27017)])
        self.assertEqual(result["username"], "admin")
        self.assertEqual(result["password"], "pass")
        self.assertEqual(result["database"], "main")
        self.assertEqual(result["options"], {})
