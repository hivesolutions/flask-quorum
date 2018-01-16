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

import flask

import quorum

class AclTest(quorum.TestCase):

    def setUp(self):
        try:
            self.app = quorum.load(
                name = __name__,
                secret_key = "secret"
            )
        except:
            self.skip()

    def tearDown(self):
        quorum.unload()

    @quorum.secured
    def test_check_login(self):
        with self.app.test_client() as client:
            client.get("/")

            flask.session["tokens"] = ["*"]
            result = quorum.check_login(token = "admin")
            self.assertEqual(result, True)
            self.assertEqual(flask.session["tokens"], {"*" : True})

            flask.session["tokens"] = []
            result = quorum.check_login(token = "admin")
            self.assertEqual(result, False)
            self.assertEqual(flask.session["tokens"], {})

            flask.session["tokens"] = ["admin"]
            result = quorum.check_login(token = "admin")
            self.assertEqual(result, True)
            self.assertEqual(flask.session["tokens"], {"admin" : True})

            flask.session["tokens"] = ["admin.read"]
            result = quorum.check_login(token = "admin")
            self.assertEqual(result, False)
            result = quorum.check_login(token = "admin.read")
            self.assertEqual(result, True)
            self.assertEqual(flask.session["tokens"], {
                "admin" : {
                    "read" : True
                }
            })

            flask.session["tokens"] = ["admin.*"]
            result = quorum.check_login(token = "admin.read")
            self.assertEqual(result, True)
            self.assertEqual(flask.session["tokens"], {
                "admin" : {
                    "*" : True
                }
            })

            flask.session["tokens"] = ["admin", "admin.write"]
            result = quorum.check_login(token = "admin.read")
            self.assertEqual(result, False)
            self.assertEqual(flask.session["tokens"], {
                "admin" : {
                    "_" : True,
                    "write" : True
                }
            })

            flask.session["tokens"] = ["admin.write", "admin.*"]
            result = quorum.check_login(token = "admin.read")
            self.assertEqual(result, True)
            self.assertEqual(flask.session["tokens"], {
                "admin" : {
                    "write" : True,
                    "*" : True
                }
            })

            del flask.session["tokens"]
            result = quorum.check_login(token = "admin.read")
            self.assertEqual(result, False)
            self.assertEqual("tokens" in flask.session, False)

    @quorum.secured
    def test_check_tokens(self):
        result = quorum.check_tokens(("admin", "user"), tokens_m = {"*" : True})
        self.assertEqual(result, True)

        result = quorum.check_tokens(("admin", "user"), tokens_m = {})
        self.assertEqual(result, False)

        result = quorum.check_tokens(("admin", "user"), tokens_m = {"admin" : True})
        self.assertEqual(result, False)

    @quorum.secured
    def test_check_token(self):
        result = quorum.check_token("admin", tokens_m = {"*" : True})
        self.assertEqual(result, True)

        result = quorum.check_token("admin", tokens_m = {})
        self.assertEqual(result, False)

        result = quorum.check_token("admin", tokens_m = {"admin" : True})
        self.assertEqual(result, True)

        result = quorum.check_token("admin.read", tokens_m = {
            "admin" : {
                "read" : True
            }
        })
        self.assertEqual(result, True)

        result = quorum.check_token("admin", tokens_m = {
            "admin" : {
                "read" : True
            }
        })
        self.assertEqual(result, False)

        result = quorum.check_token("admin.read", tokens_m = {
            "admin" : {
                "*" : True
            }
        })
        self.assertEqual(result, True)

        result = quorum.check_token(None, tokens_m = {})
        self.assertEqual(result, True)

    def test_to_tokens_m(self):
        result = quorum.to_tokens_m(["admin"])
        self.assertEqual(result, {"admin" : True})

        result = quorum.to_tokens_m(["admin", "admin.read"])
        self.assertEqual(result, {
            "admin" : {
                "_" : True,
                "read" : True
            }
        })

        result = quorum.to_tokens_m(["admin.read", "admin"])
        self.assertEqual(result, {
            "admin" : {
                "_" : True,
                "read" : True
            }
        })

        result = quorum.to_tokens_m(["admin", "admin.*"])
        self.assertEqual(result, {
            "admin" : {
                "_" : True,
                "*" : True
            }
        })
