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

YEAR_IN_SECS = 31536000
""" The number of seconds that exist in a
complete year (365 days) """

class SSLify(object):
    """
    Secures your flask app by enabling the forcing
    of the protocol in the HTTP connection.
    """

    def __init__(self, app, age = YEAR_IN_SECS, subdomains = False):
        """
        Constructor of the class.

        :type app: App
        :param app: The application object to be used in the
        in ssl operation for the forcing of the protocol.
        :type age: int
        :param age: The maximum age of the hsts operation.
        :type subdomains: bool
        :param subdomains: If subdomain should be allows as part
        of the security policy.
        """

        if not app == None:
            self.app = app
            self.hsts_age = age
            self.hsts_include_subdomains = subdomains

            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        """
        Configures the configured flask app to enforce ssl.

        :type app: App
        :param app: The application to be configured to enforce
        the ssl redirection support.
        """

        app.before_request(self.redirect_to_ssl)
        app.after_request(self.set_hsts_header)

    @property
    def hsts_header(self):
        """
        Returns the proper hsts policy.

        :rtype: String
        :return: The proper hsts policy string value.
        """

        hsts_policy = "max-age={0}".format(self.hsts_age)
        if self.hsts_include_subdomains: hsts_policy += "; includeSubDomains"

        return hsts_policy

    def redirect_to_ssl(self):
        """
        Redirect incoming requests to HTTPS in case the current
        protocol is not considered secure.

        This is a conditional execution that verifies the current
        request against any of the defined rules of security.

        :rtype: Request
        :return: The changed request containing the redirect
        instruction in case it's required.
        """

        criteria = [
            flask.request.is_secure,
            flask.request.headers.get("X-Forwarded-Proto", "http") == "https"
        ]

        if any(criteria): return
        if not flask.request.url.startswith("http://"): return

        url = flask.request.url.replace("http://", "https://", 1)
        request = flask.redirect(url)
        return request

    def set_hsts_header(self, response):
        """
        Adds hsts header to each response, that should be performed
        at the end of the request handling workflow.

        This header should enable extra security options to be
        interpreted at the client side.

        :type response: Response
        :param response: The response to be used to set the hsts
        policy header.
        :rtype: Response
        :return: The changed response object, containing the strict
        transport security (hsts) header.
        """

        response.headers.setdefault("Strict-Transport-Security", self.hsts_header)
        return response
