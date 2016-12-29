#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2017 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import quorum

class AmazonTest(quorum.TestCase):

    def setUp(self):
        try:
            quorum.load(
                name = __name__
            )
            quorum.get_amazon()
        except:
            self.skip()

    def tearDown(self):
        try: quorum.clear_amazon_bucket()
        except: pass
        finally: quorum.unload()

    @quorum.secured
    def test_connect(self):
        connection = quorum.get_amazon()
        self.assertNotEqual(connection, None)

    @quorum.secured
    def test_bucket(self):
        bucket = quorum.get_amazon_bucket()
        self.assertNotEqual(bucket, None)

    @quorum.secured
    def test_key(self):
        key = quorum.get_amazon_key("test")
        key.set_contents_from_string("test message")

        key = quorum.get_amazon_key("test")
        value = key.get_contents_as_string()
        self.assertEqual(value, "test message")

        value = quorum.exists_amazon_key("test")
        self.assertEqual(value, True)

        quorum.delete_amazon_key("test")

        value = quorum.exists_amazon_key("test")
        self.assertEqual(value, False)
