#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2016 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import quorum

class HttpcTest(quorum.TestCase):

    @quorum.secured
    def test_parse_url(self):
        url, scheme, host, authorization, params = quorum.httpc._parse_url("http://hive.pt/")

        self.assertEqual(url, "http://hive.pt:80/")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, None)
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url("http://username@hive.pt/")

        self.assertEqual(url, "http://hive.pt:80/")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, None)
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url("http://username:password@hive.pt/")

        self.assertEqual(url, "http://hive.pt:80/")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, "dXNlcm5hbWU6cGFzc3dvcmQ=")
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url("http://username:password@hive.pt/hello/world")

        self.assertEqual(url, "http://hive.pt:80/hello/world")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, "dXNlcm5hbWU6cGFzc3dvcmQ=")
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url("http://username:password@hive.pt/hello/world?hello=world")

        self.assertEqual(url, "http://hive.pt:80/hello/world")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, "dXNlcm5hbWU6cGFzc3dvcmQ=")
        self.assertEqual(params, dict(hello = ["world"]))

    @quorum.secured
    def test_redirect(self):
        _data, response = quorum.get_json(
            "http://httpbin.org/redirect-to?url=https%3a%2f%2Fhttpbin.org%2f",
            handle = True,
            redirect = True
        )

        code = response.getcode()
        self.assertNotEqual(code, 302)
        self.assertEqual(code, 200)

        _data, response = quorum.get_json(
            "https://httpbin.org/relative-redirect/2",
            handle = True,
            redirect = True
        )

        code = response.getcode()
        self.assertNotEqual(code, 302)
        self.assertEqual(code, 200)

    @quorum.secured
    def test_get_f(self):
        file = quorum.get_f("https://httpbin.org/image/png")

        self.assertEqual(file.file_name, "default")
        self.assertEqual(file.mime, "image/png")
        self.assertEqual(len(file.data) > 100, True)
        self.assertEqual(len(file.data_b64) > 100, True)

        file = quorum.get_f("https://httpbin.org/image/png", name = "dummy")

        self.assertEqual(file.file_name, "dummy")
        self.assertEqual(file.mime, "image/png")
        self.assertEqual(len(file.data) > 100, True)
        self.assertEqual(len(file.data_b64) > 100, True)
