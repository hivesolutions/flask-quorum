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

import threading

import quorum


class HTTPCTest(quorum.TestCase):

    def setUp(self):
        quorum.TestCase.setUp(self)
        self.httpbin = quorum.conf("HTTPBIN", "httpbin.org")

    @quorum.secured
    def test_basic_auth(self):
        result = quorum.httpc.basic_auth("username", "password")

        self.assertEqual(result, "Basic dXNlcm5hbWU6cGFzc3dvcmQ=")
        self.assertEqual(quorum.legacy.is_string(result), True)

        result_single = quorum.httpc.basic_auth("username")
        result_multiple = quorum.httpc.basic_auth("username", "username")

        self.assertEqual(result_single, "Basic dXNlcm5hbWU6dXNlcm5hbWU=")
        self.assertEqual(quorum.legacy.is_string(result), True)
        self.assertEqual(result_single, result_multiple)

    @quorum.secured
    def test__parse_url(self):
        url, scheme, host, authorization, params = quorum.httpc._parse_url(
            "http://hive.pt/"
        )

        self.assertEqual(url, "http://hive.pt:80/")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, None)
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url(
            "http://username@hive.pt/"
        )

        self.assertEqual(url, "http://hive.pt:80/")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, None)
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url(
            "http://username:password@hive.pt/"
        )

        self.assertEqual(url, "http://hive.pt:80/")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, "dXNlcm5hbWU6cGFzc3dvcmQ=")
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url(
            "http://username:password@hive.pt/hello/world"
        )

        self.assertEqual(url, "http://hive.pt:80/hello/world")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, "dXNlcm5hbWU6cGFzc3dvcmQ=")
        self.assertEqual(params, {})

        url, scheme, host, authorization, params = quorum.httpc._parse_url(
            "http://username:password@hive.pt/hello/world?hello=world"
        )

        self.assertEqual(url, "http://hive.pt:80/hello/world")
        self.assertEqual(scheme, "http")
        self.assertEqual(host, "hive.pt")
        self.assertEqual(authorization, "dXNlcm5hbWU6cGFzc3dvcmQ=")
        self.assertEqual(params, dict(hello=["world"]))

    @quorum.secured
    def test_redirect(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        quoted = quorum.legacy.quote("https://%s/" % self.httpbin)
        _data, response = quorum.get_json(
            "https://%s/redirect-to?url=%s" % (self.httpbin, quoted),
            handle=True,
            redirect=True,
        )

        code = response.getcode()
        self.assertNotEqual(code, 302)
        self.assertEqual(code, 200)

        _data, response = quorum.get_json(
            "https://%s/relative-redirect/2" % self.httpbin, handle=True, redirect=True
        )

        code = response.getcode()
        self.assertNotEqual(code, 302)
        self.assertEqual(code, 200)

    @quorum.secured
    def test_timeout(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        self.assertRaises(
            BaseException,
            lambda: quorum.get_json(
                "https://%s/delay/3" % self.httpbin,
                handle=True,
                redirect=True,
                timeout=1,
            ),
        )

        data, response = quorum.get_json(
            "https://%s/delay/1" % self.httpbin, handle=True, redirect=True, timeout=30
        )

        code = response.getcode()
        self.assertEqual(code, 200)
        self.assertNotEqual(len(data), 0)
        self.assertNotEqual(data, None)

    @quorum.secured
    def test_get_f(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        file = quorum.get_f("https://%s/image/png" % self.httpbin)

        self.assertEqual(file.file_name, "default")
        self.assertEqual(file.mime, "image/png")
        self.assertEqual(len(file.data) > 100, True)
        self.assertEqual(len(file.data_b64) > 100, True)

        file = quorum.get_f("https://%s/image/png" % self.httpbin, name="dummy")

        self.assertEqual(file.file_name, "dummy")
        self.assertEqual(file.mime, "image/png")
        self.assertEqual(len(file.data) > 100, True)
        self.assertEqual(len(file.data_b64) > 100, True)

    @quorum.secured
    def test_generator(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        def text_g(message=[b"hello", b" ", b"world"]):
            yield sum(len(value) for value in message)
            for value in message:
                yield value

        data, response = quorum.post_json(
            "https://%s/post" % self.httpbin, data=text_g(), handle=True, reuse=False
        )

        code = response.getcode()
        self.assertNotEqual(code, 302)
        self.assertEqual(code, 200)
        self.assertEqual(data["data"], "hello world")

    @quorum.secured
    def test_file(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        data, response = quorum.post_json(
            "https://%s/post" % self.httpbin,
            data=quorum.legacy.BytesIO(b"hello world"),
            handle=True,
            reuse=False,
        )

        code = response.getcode()
        self.assertNotEqual(code, 302)
        self.assertEqual(code, 200)
        self.assertEqual(data["data"], "hello world")

    @quorum.secured
    def test_multithread(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        threads = []
        results = []

        for index in range(10):
            result = dict()
            results.append(result)

            def generate(index):
                def caller():
                    data, response = quorum.get_json(
                        "https://%s/ip" % self.httpbin, handle=True
                    )
                    result = results[index]
                    result["data"] = data
                    result["response"] = response

                return caller

            callable = generate(index)
            thread = threading.Thread(target=callable, name="TestMultithread")
            thread.start()
            threads.append(thread)

        for thread, result in zip(threads, results):
            thread.join()

            response = result["response"]
            code = response.getcode()
            self.assertNotEqual(code, 302)
            self.assertEqual(code, 200)

    @quorum.secured
    def test_error(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        self.assertRaises(
            quorum.HTTPDataError,
            lambda: quorum.get("https://%s/status/404" % self.httpbin),
        )

    @quorum.secured
    def test_invalid(self):
        if quorum.conf("NO_NETWORK", False, cast=bool):
            self.skipTest("Network access is disabled")

        self.assertRaises(
            BaseException, lambda: quorum.get("https://invalidlargedomain.org/")
        )
