#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (C) 2008-2012 Hive Solutions Lda.
#
# This file is part of Hive Flask Quorum.
#
# Hive Flask Quorum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Flask Quorum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Flask Quorum. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import flask
import smtplib

import email.mime.multipart
import email.mime.text

import base
import execution

SMTP_HOST = "localhost"
""" The host to be used in the smtp connection with
the remote host """

SMTP_USER = None
""" The used to be used in authentication with the
smtp remote host """

SMTP_PASSWORD = None
""" The password to be used in the authentication with
the remote smtp server """

def send_mail(app = None, subject = "", sender = None, receivers = [], data = None, plain = None, rich = None, context = {}):
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
    """

    app = app or base.APP

    # sets the sender with the smtp user value in case no values
    # has been provided (expected behavior)
    sender = sender or SMTP_USER

    # renders the (possible existing) templates in both the plain
    # and rich text object retrieving the final data to be sent
    plain_data = plain and _render(app, plain, **context) or data
    html_data = rich and _render(app, rich, **context) or data

    # creates the mime's multipart object with the appropriate header
    # values set and in the alternative model (for html compatibility)
    message = email.mime.multipart.MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(receivers)

    # creates both the plain text and the rich text (html) objects
    # from the provided data and then attached them to the message
    # (multipart alternative) that is the base structure
    plain = plain_data and email.mime.text.MIMEText(plain_data, "plain")
    html = html_data and email.mime.text.MIMEText(html_data, "html")
    plain and message.attach(plain)
    html and message.attach(html)

    # creates the connection with the smtp server and starts the tls
    # connection to send the created email message
    server = smtplib.SMTP(SMTP_HOST)
    try:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(sender, receivers, message.as_string())
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

def _render(app, template_name, **context):
    template = app.jinja_env.get_or_select_template(template_name)
    return flask.templating._render(template, context, app)
