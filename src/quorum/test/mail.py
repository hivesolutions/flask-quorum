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

import quorum.mail

class MailTest(quorum.TestCase):

    def setUp(self):
        try: quorum.load(name = __name__)
        except: self.skip()

    def tearDown(self):
        quorum.unload()

    @quorum.secured
    def test_format(self):
        result = quorum.mail._format("João Magalhães <joamag@hive.pt>")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "=?utf-8?q?Jo=C3=A3o_Magalh=C3=A3es?= <joamag@hive.pt>")

        result = quorum.mail._format(u"João Magalhães <joamag@hive.pt>")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "=?utf-8?q?Jo=C3=A3o_Magalh=C3=A3es?= <joamag@hive.pt>")

        result = quorum.mail._format(u"若昂·马加良斯 <joamag@hive.pt>")
        self.assertEqual(type(result), str)
        self.assertEqual(result, "=?utf-8?b?6Iul5piCwrfpqazliqDoia/mlq8=?= <joamag@hive.pt>")
