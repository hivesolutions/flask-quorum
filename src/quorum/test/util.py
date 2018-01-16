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

import string

import quorum

class UtilTest(quorum.TestCase):

    def setUp(self):
        try:
            quorum.load(name = __name__)
        except:
            self.skip()

    def tearDown(self):
        quorum.unload()

    @quorum.secured
    def test_is_mobile(self):
        result = quorum.is_mobile(user_agent = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19")
        self.assertEqual(result, True)

        result = quorum.is_mobile(user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        self.assertEqual(result, True)

        result = quorum.is_mobile(user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12")
        self.assertEqual(result, False)

        result = quorum.is_mobile(user_agent = "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30")
        self.assertEqual(result, False)

        result = quorum.is_mobile(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        self.assertEqual(result, False)

        result = quorum.is_mobile(user_agent = "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1")
        self.assertEqual(result, False)

        result = quorum.is_mobile(user_agent = "")
        self.assertEqual(result, False)

    @quorum.secured
    def test_is_tablet(self):
        result = quorum.is_tablet(user_agent = "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1")
        self.assertEqual(result, True)

        result = quorum.is_tablet(user_agent = "Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329")
        self.assertEqual(result, True)

        result = quorum.is_tablet(user_agent = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19")
        self.assertEqual(result, True)

        result = quorum.is_tablet(user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        self.assertEqual(result, True)

        result = quorum.is_tablet(user_agent = "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30")
        self.assertEqual(result, True)

        result = quorum.is_tablet(user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12")
        self.assertEqual(result, False)

        result = quorum.is_tablet(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        self.assertEqual(result, False)

        result = quorum.is_tablet(user_agent = "")
        self.assertEqual(result, False)

    @quorum.secured
    def test_is_browser(self):
        result = quorum.is_browser(user_agent = "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136")
        self.assertEqual(result, True)

        result = quorum.is_browser(user_agent = "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)")
        self.assertEqual(result, False)

        result = quorum.is_browser(user_agent = "netius/1.1.10")
        self.assertEqual(result, False)

        result = quorum.is_browser(user_agent = "")
        self.assertEqual(result, False)

    @quorum.secured
    def test_is_bot(self):
        result = quorum.is_bot(user_agent = "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10B329")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "Mozilla/5.0 (Linux; U; Android 4.1.1; en-gb; Build/KLP) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)")
        self.assertEqual(result, True)

        result = quorum.is_bot(user_agent = "netius/1.1.10")
        self.assertEqual(result, False)

        result = quorum.is_bot(user_agent = "")
        self.assertEqual(result, False)

    @quorum.secured
    def test_browser_info(self):
        result = quorum.browser_info(user_agent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136")
        self.assertEqual(result, dict(
            name = "Edge",
            version = "12.10136",
            version_f = 12.10136,
            version_i = 12,
            interactive = True,
            bot = False,
            os = "Windows"
        ))

        result = quorum.browser_info(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36")
        self.assertEqual(result, dict(
            name = "Chrome",
            version = "62.0.3202.75",
            version_f = 62.0,
            version_i = 62,
            interactive = True,
            bot = False,
            os = "Windows"
        ))

        result = quorum.browser_info(user_agent = "Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1")
        self.assertEqual(result, dict(
            name = "Safari",
            version = "601.1",
            version_f = 601.1,
            version_i = 601,
            interactive = True,
            bot = False,
            os = "Mac"
        ))

        result = quorum.browser_info(user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0")
        self.assertEqual(result, dict(
            name = "Firefox",
            version = "56.0",
            version_f = 56.0,
            version_i = 56,
            interactive = True,
            bot = False,
            os = "Windows"
        ))

        result = quorum.browser_info(user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)")
        self.assertEqual(result, dict(
            name = "Explorer",
            version = "8.0",
            version_f = 8.0,
            version_i = 8,
            interactive = True,
            bot = False,
            os = "Windows"
        ))

        result = quorum.browser_info(user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
        self.assertEqual(result, dict(
            name = "Googlebot",
            version = "2.1",
            version_f = 2.1,
            version_i = 2,
            interactive = False,
            bot = True
        ))

        result = quorum.browser_info(user_agent = "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)")
        self.assertEqual(result, dict(
            name = "Bingbot",
            version = "2.0",
            version_f = 2.0,
            version_i = 2,
            interactive = False,
            bot = True
        ))

        result = quorum.browser_info(user_agent = "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)")
        self.assertEqual(result, dict(
            name = "DuckDuckBot",
            version = "1.0",
            version_f = 1.0,
            version_i = 1,
            interactive = False,
            bot = True
        ))

        result = quorum.browser_info(user_agent = "netius/1.1.10")
        self.assertEqual(result, dict(
            name = "netius",
            version = "1.1.10",
            version_f = 1.1,
            version_i = 1,
            interactive = False,
            bot = False
        ))

        result = quorum.browser_info(user_agent = "APIs-Google (+https://developers.google.com/webmasters/APIs-Google.html)")
        self.assertEqual(result, None)

    @quorum.secured
    def test_camel_to_underscore(self):
        result = quorum.camel_to_underscore("HelloWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "hello_world")

        result = quorum.camel_to_underscore("HELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "hello_world")

        result = quorum.camel_to_underscore("HELLOWorldHELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "hello_world_hello_world")

    @quorum.secured
    def test_camel_to_readable(self):
        result = quorum.camel_to_readable("HelloWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.camel_to_readable("HelloWorld", lower = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world")

        result = quorum.camel_to_readable("HelloWorld", lower = True, capitalize = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.camel_to_readable("HELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "HELLO World")

        result = quorum.camel_to_readable("HELLOWorld", lower = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world")

        result = quorum.camel_to_readable(
            "HELLOWorld",
            lower = True,
            capitalize = True
        )
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.camel_to_readable("HELLOWorldHELLOWorld")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "HELLO World HELLO World")

        result = quorum.camel_to_readable(
            "HELLOWorldHELLOWorld",
            lower = True
        )
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world hello world")

        result = quorum.camel_to_readable(
            "HELLOWorldHELLOWorld",
            lower = True,
            capitalize = True
        )
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World Hello World")

    @quorum.secured
    def test_underscore_to_readable(self):
        result = quorum.underscore_to_readable("hello_world")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world")

        result = quorum.underscore_to_readable("hello_world", capitalize = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World")

        result = quorum.underscore_to_readable("hello_world_hello_world")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello world hello world")

        result = quorum.underscore_to_readable("hello_world_hello_world", capitalize = True)
        self.assertEqual(type(result), str)
        self.assertEqual(result, "Hello World Hello World")

    @quorum.secured
    def test_generate_identifier(self):
        identifier = quorum.generate_identifier(
            size = 16,
            chars = string.ascii_uppercase
        )
        self.assertEqual(len(identifier), 16)
        for char in identifier:
            self.assertTrue(char in string.ascii_uppercase)

    @quorum.secured
    def test_is_content_type(self):
        result = quorum.is_content_type("text/plain", "text/plain")
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/plain", ("text/plain",))
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/plain", "text/html")
        self.assertEqual(result, False)

        result = quorum.is_content_type("text/plain", ("text/html",))
        self.assertEqual(result, False)

        result = quorum.is_content_type("text/plain", ("text/plain", "text/html"))
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/*", "text/plain")
        self.assertEqual(result, True)

        result = quorum.is_content_type("text/*", "text/json")
        self.assertEqual(result, True)

    @quorum.secured
    def test_parse_content_type(self):
        result = quorum.parse_content_type("text/plain")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain"])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text/plain+json")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text/plain+json; charset=utf-8")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict(charset = "utf-8"))

        result = quorum.parse_content_type("text/plain+json   ; charset=utf-8")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict(charset = "utf-8"))

        result = quorum.parse_content_type("text/plain+json; charset=utf-8; boundary=hello;")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict(charset = "utf-8", boundary = "hello"))

        result = quorum.parse_content_type("")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [])
        self.assertEqual(result[1], dict())

        result = quorum.parse_content_type("text/plain+json; charset")
        self.assertEqual(type(result), tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["text/plain", "text/json"])
        self.assertEqual(result[1], dict())
