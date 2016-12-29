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

import flask
import smtplib

import email.utils
import email.header

import email.mime.multipart
import email.mime.text

from . import config
from . import common
from . import legacy
from . import execution

def send_mail(
    app = None,
    subject = "",
    sender = None,
    receivers = [],
    data = None,
    plain = None,
    rich = None,
    context = {},
    encoding = "utf-8",
    host = None,
    port = None,
    username = None,
    password = None,
    stls = False,
    safe = True
):
    """
    Sends an email message using the provided :rst:dir:`SMTP_HOST`,
    :rst:dir:`SMTP_USER` and :rst:dir:`SMTP_PASSWORD` configurations.

    The email message is sent under the ``alternative`` mime
    type so that both the plain text and the rich text (html)
    parts are sent in the same message.

    The ``plain`` and ``rich`` arguments allow the user to process
    a template with the context provided by the ``context`` map.

    .. warning::

        This is a blocking call and as such the control flow may block
        for more that a second, if you want a non blocking (asynchronous)
        call please use :func:`quorum.send_mail_a`.

    :type app: Application
    :param app: Optional application object to be used for the\
    rendering operation as the main object for flask. In case this\
    value is not provided the global :attr:`quorum.APP` value is\
    used instead (fallback).
    :type subject: String
    :param subject: The mime subject to be sent with this message,\
    note that if this value is not set many spam filters will consider\
    the message as spam.
    :type sender: String
    :param sender: The email (and name) of the sender of the email, in\
    case this value is not set the :rst:dir:`SMTP_USER` variable is\
    used instead.
    :type receivers: List
    :param receivers: The list of receivers (with email and name) for\
    which the email will be sent.
    :type data: String
    :param data: The buffer containing the data to be used for both the\
    plain and the rich text parts in case the template associated arguments\
    are not set or in case the rendering is not successful.
    :type plain: String
    :param plain: Relative path to the plain text template to be used\
    for the rendering of the email, this path must be relative to the\
    templates folder.
    :type rich: String
    :param rich: Relative path to the rich text template to be used\
    for the rendering of the email, this path must be relative to the\
    templates folder.
    :type context: Dictionary
    :param context: The map containing the complete set of variables that\
    are going to be `"exposed"` to the template rendering engine for both\
    the ``plain`` and the ``rich``.
    :type encoding: String
    :param encoding: The text encoding name that is going to be used in the\
    mail that is going to be sent, should be used with care.
    :type host: String
    :param host: The hostname for the connection of the smtp server that\
    is going to be used, this may be wither a domain of an address.
    :type port: int
    :param port: The tcp port number that is going to be used for the client\
    connection with the server.
    :type username: String
    :param username: Username value that is used for the authentication part\
    of the connection with the smtp server.
    :type password: String
    :param password: Secret password to be used as part of the authentication\
    process of the created smtp connection.
    :type stls: bool
    :param stls: If the connection with the target smtp server should be made\
    using a secure mechanism of a plain text one.
    :type safe: bool
    :param safe: If the current email message should be used using a safe\
    strategy, meaning that newline sequences will be made standard.
    """

    # retrieves the reference to the currently loaded/defined application
    # from the "global" common module (dynamic loading)
    app = app or common.base().APP

    # retrieved the default value of the data value so that no part of
    # the email is left empty (required by specification)
    data = data or "This part of the email is empty"

    # tries to retrieve the various configuration values that are going
    # to be used for the establishment of the smtp connection, taking
    # into account both the provided parameters and the configuration
    # variables currently defined for the environment
    host = host or config.conf("SMTP_HOST", "localhost")
    port = port or config.conf("SMTP_PORT", 25, cast = int)
    username = username or config.conf("SMTP_USER", None)
    password = password or config.conf("SMTP_PASSWORD", None)
    stls = password or stls or config.conf("SMTP_STARTTLS", True, cast = int)

    # sets the sender with the smtp user value in case no values
    # has been provided (expected behavior)
    sender = sender or username

    # renders the (possible existing) templates in both the plain
    # and rich text object retrieving the final data to be sent
    plain_data = plain and _render(app, plain, **context) or data
    html_data = rich and _render(app, rich, **context) or data

    # verifies the existence of data (both plain and html) and in
    # there's data it should be encoded using the currently provided
    # one so that the raw data is used instead of the unicode one
    if plain_data: plain_data = plain_data.encode(encoding)
    if html_data: html_data = html_data.encode(encoding)

    # creates the mime's multipart object with the appropriate header
    # values set and in the alternative model (for html compatibility)
    message = _multipart()
    message["Subject"] = subject
    message["From"] = _format(sender)
    message["To"] = ", ".join(_format(receiver) for receiver in receivers)

    # creates both the plain text and the rich text (html) objects
    # from the provided data and then attached them to the message
    # (multipart alternative) that is the base structure
    plain = plain_data and _plain(plain_data, encoding = encoding)
    html = html_data and _html(html_data, encoding = encoding)
    plain and message.attach(plain)
    html and message.attach(html)

    # converts the created message into a plain string value and then
    # in case the safe flag is active replaces the proper newline
    # sequences so that the mail string is made standard
    contents = message.as_string()
    if safe:
        contents = contents.replace("\r\n", "\n")
        contents = contents.replace("\n", "\r\n")

    # creates the connection with the smtp server and starts the tls
    # connection to send the created email message
    server = smtplib.SMTP(host, port = port)
    try:
        if stls: server.starttls()
        server.login(username, password)
        server.sendmail(sender, receivers, contents)
    finally:
        server.quit()

def send_mail_a(*args, **kwargs):
    """
    Asynchronous call to the :func:`quorum.send_mail` function that
    is executed in a different thread from the current one. The currently
    loaded queue system is used for the sending of the email, for more
    information check on :func:`quorum.run_background` .

    .. note::

        The arguments to be send for this function are the same as the one
        present in the original :func:`quorum.send_mail` function.
    """

    execution.insert_work(send_mail, args, kwargs)

def _multipart():
    return email.mime.multipart.MIMEMultipart("alternative")

def _plain(contents, encoding = "utf-8"):
    return email.mime.text.MIMEText(contents, "plain", encoding)

def _html(contents, encoding = "utf-8"):
    return email.mime.text.MIMEText(contents, "html", encoding)

def _format(address, encoding = "utf-8"):
    address_name, address_email = email.utils.parseaddr(address)
    if legacy.is_bytes(address_name): address_name = address_name.decode(encoding)
    address_name = email.header.Header(address_name, charset = encoding)
    address_name = address_name.encode()
    address_email = str(address_email)
    return "%s <%s>" % (address_name, address_email)

def _render(app, template_name, **context):
    template = app.jinja_env.get_or_select_template(template_name)
    return flask.templating._render(template, context, app)
