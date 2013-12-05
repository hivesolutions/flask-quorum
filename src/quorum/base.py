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

import os
import sys
import json
import flask
import atexit
import logging
import inspect

import acl
import log
import util
import mail
import route
import model
import amazon
import extras
import config
import session
import redisdb
import mongodb
import pusherc
import request
import rabbitmq
import execution
import exceptions

APP = None
""" The reference to the top level application
that is being handled by quorum """

RUN_CALLED = False
""" Flag that controls if the on run methods have already
been called for the current execution environment """

RUN_F = {}
""" The map that will contain the various functions that
will be called upon the start of the main run loop """

LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
""" The logging format definition to be used by all
the format handlers available, this string will also
be used under the log module for handlers """

def call_run():
    global RUN_CALLED
    if RUN_CALLED: return
    for _fname, f in RUN_F.iteritems(): f()
    RUN_CALLED = True

def run(server = None, fallback = "base"):
    if not APP: raise exceptions.BaseError("Application not set or runnable")

    server = config.conf("SERVER", server) or "base"
    runner = globals().get("run_" + server, None)
    runner_f = globals().get("run_" + fallback, None)
    if not runner: raise exceptions.BaseError("Server '%s' not found" % server)

    call_run()

    try: runner()
    except exceptions.ServerInitError, error:
        APP.logger.warn(
            "Server '%s' failed to start (%s) falling back to '%s'" % (
                server, unicode(error), fallback
            )
        )
        runner_f and runner_f()

def run_base():
    debug = config.conf("DEBUG", False, cast = bool)
    reloader = config.conf("RELOADER", False, cast = bool)
    host = config.conf("HOST", "127.0.0.1")
    port = int(config.conf("PORT", 5000))
    APP.run(
        use_debugger = debug,
        debug = debug,
        use_reloader = reloader,
        host = host,
        port = port
    )

def run_waitress():
    try: import waitress
    except BaseException, exception:
        raise exceptions.ServerInitError(
            unicode(exception),
            server = "waitress"
        )

    host = config.conf("HOST", "127.0.0.1")
    port = int(config.conf("PORT", 5000))
    waitress.serve(
        APP,
        host = host,
        port = port
    )

def run_netius():
    try: import netius.servers
    except BaseException, exception:
        raise exceptions.ServerInitError(
            unicode(exception),
            server = "netius"
        )

    kwargs = dict()
    host = config.conf("HOST", "127.0.0.1")
    port = int(config.conf("PORT", 5000))
    ssl = int(config.conf("SSL", 0)) and True or False
    key_file = config.conf("KEY_FILE", None)
    cer_file = config.conf("CER_FILE", None)
    servers = config.conf_prefix("SERVER_")
    for name, value in servers.iteritems():
        name_s = name.lower()[7:]
        kwargs[name_s] = value
    server = netius.servers.WSGIServer(APP, **kwargs)
    server.serve(
        host = host,
        port = port,
        ssl = ssl,
        key_file = key_file,
        cer_file = cer_file
    )

def load(app = None, name = None, secret_key = None, execution = True, redis_session = False,\
    mongo_database = None, logger = None, models = None, **kwargs):
    """
    Initial loader function responsible for the overriding of
    the flask loading system and for the loading of configuration.

    .. note::

        This function should be called inside you main app file failure
        to do so may result in unexpected behavior.

    :type app: Application
    :param app: The optional flask application object to be used\
    in the loading of quorum (useful for self managed apps).
    :type name: String
    :param name: The name to be used to describe the application\
    for the management of internal values.
    :type secret_key: String
    :param secret_key: The secret seed value to be used for cryptographic\
    operations under flask (eg: client side sessions) this value should\
    be shared among all the pre-fork instances.
    :type execution: bool
    :param execution: Flag indicating if the (background) execution thread\
    should be started providing the required support for background tasks.
    :type redis_session: bool
    :param redis_session: If the session management for the flask infra-structure\
    should be managed using a server side session with support from redis.
    :type mongo_database: String
    :param mongo_database: The default name of the database to be used when\
    using the mongo infra-structure.
    :type logger: String
    :param logger: The name to be used as identification for possible logger\
    files created by the logging sub-module.
    :type models: Module
    :param models: The module containing the complete set of model classes to\
    be used by the data infra-structure (eg: ``mongo``).
    :rtype: Application
    :return: The application that is used by the loaded quorum environment in\
    case one was provided that is retrieved, otherwise the newly created one is\
    returned instead.
    """

    global APP
    if APP: return APP

    app = app or flask.Flask(name)

    load_all()
    load_app_config(app, kwargs)
    debug = config.conf("DEBUG", False, cast = bool)
    force_ssl = config.conf("FORCE_SSL", False)
    redis_url = config.conf("REDISTOGO_URL", None)
    mongo_url = config.conf("MONGOHQ_URL", None)
    rabbit_url = config.conf("CLOUDAMQP_URL", None)
    amazon_id = config.conf("AMAZON_ID", None)
    amazon_secret = config.conf("AMAZON_SECRET", None)
    amazon_bucket = config.conf("AMAZON_BUCKET", None)
    pusher_app_id = config.conf("PUSHER_APP_ID", None)
    pusher_key = config.conf("PUSHER_KEY", None)
    pusher_secret = config.conf("PUSHER_SECRET", None)
    smtp_host = config.conf("SMTP_HOST", None)
    smtp_user = config.conf("SMTP_USER", None)
    smtp_password = config.conf("SMTP_PASSWORD", None)
    level = debug and logging.DEBUG or logging.WARN

    start_log(app, name = logger, level = level)
    if redis_url: redisdb.url = redis_url
    if mongo_url: mongodb.url = mongo_url
    if rabbit_url: rabbitmq.url = rabbit_url
    if amazon_id: amazon.id = amazon_id
    if amazon_secret: amazon.secret = amazon_secret
    if amazon_bucket: amazon.bucket_name = amazon_bucket
    if pusher_app_id: pusherc.app_id = pusher_app_id
    if pusher_key: pusherc.key = pusher_key
    if pusher_secret: pusherc.secret = pusher_secret
    if smtp_host: mail.SMTP_HOST = smtp_host
    if smtp_user: mail.SMTP_USER = smtp_user
    if smtp_password: mail.SMTP_PASSWORD = smtp_password
    if execution: start_execution()
    if redis_session: app.session_interface = session.RedisSessionInterface(url = redis_url)
    if mongo_database: mongodb.database = mongo_database
    if models: setup_models(models)
    if force_ssl: extras.SSLify(app)
    app.before_request(before_request)
    app.context_processor(context_processor)
    app.request_class = request.Request
    app.debug = debug
    app.models = models
    app.secret_key = secret_key
    app.old_route = app.route
    app.route = route.route
    app.jinja_options = dict(
        finalize = finalize
    )
    APP = app

    previous = inspect.stack()[1]
    module = inspect.getmodule(previous[0])
    if not module.__name__ == "__main__": call_run()

    return app

def unload():
    """
    Unloads the current quorum instance, after this call
    no more access to the quorum facilities is allowed.

    .. warning::

        Use this function with care as it may result in unexpected
        behavior from a developer point of view.

    .. note::

        After the call to this method most of the functionally of quorum\
        will become unavailable until further call to :func:`quorum.load`.
    """

    APP = None

def load_all():
    load_config(3)
    load_environ()

def load_config(offset = 1):
    element = inspect.stack()[offset]
    module = inspect.getmodule(element[0])
    base_folder = os.path.dirname(module.__file__)
    config_path = os.path.join(base_folder, "quorum.json")

    if not os.path.exists(config_path): return
    config_file = open(config_path, "rb")
    try: config.config_g = json.load(config_file)
    finally: config_file.close()

def load_environ():
    for name, value in os.environ.iteritems():
        config.config_g[name] = value

def load_app_config(app, configs):
    for name, value in configs.iteritems():
        app.config[name] = value

def start_log(app, name = None, level = logging.WARN, format = LOGGING_FORMAT):
    if os.name == "nt": path_t = "%s"
    else: path_t = "/var/log/%s"
    path = name and path_t % name

    app.handlers = {}

    formatter = logging.Formatter(format)
    logger = logging.getLogger("quorum")
    logger.parent = None
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    memory_handler = log.MemoryHandler()

    try:
        file_handler = path and logging.FileHandler(path)
    except:
        sys.stderr.write("Problem starting logging for file '%s'\n" % path)
        file_handler = None

    stream_handler and logger.addHandler(stream_handler)
    memory_handler and logger.addHandler(memory_handler)
    file_handler and logger.addHandler(file_handler)

    if stream_handler: app.handlers["stream"] = stream_handler
    if memory_handler: app.handlers["memory"] = memory_handler
    if file_handler: app.handlers["file"] = file_handler

    for handler in logger.handlers:
        handler.setFormatter(formatter)
        handler.setLevel(level)

    app.logger_q = logger

def get_log(app = None):
    app = app or APP
    is_custom = hasattr(app, "logger_q")
    return app.logger_q if is_custom else app.logger

def finalize(value):
    # returns an empty string as value representation
    # for unset values, this is the default representation
    # to be used in the template engine
    if value == None: return ""
    return value

def before_request():
    flask.request.args_s = util.load_form(flask.request.args)
    flask.request.form_s = util.load_form(flask.request.form)

def context_processor():
    return dict(
        acl = acl.check_login,
        conf = config.conf,
        nl_to_br = util.nl_to_br
    )

def start_execution():
    # creates the thread that it's going to be used to
    # execute the various background tasks and starts
    # it, providing the mechanism for execution
    execution.background_t = execution.ExecutionThread()
    execution.background_t.start()

@atexit.register
def stop_execution():
    # stop the execution thread so that it's possible to
    # the process to return the calling
    execution.background_t and execution.background_t.stop()

def setup_models(models):
    for _name, value in models.__dict__.iteritems():
        try: is_valid = issubclass(value, model.Model)
        except: is_valid = False
        if not is_valid: continue
        value.setup()

def base_path(*args, **kwargs):
    return os.path.join(APP.root_path, *args)

def onrun(function):
    fname = function.__name__
    if fname in RUN_F: return
    RUN_F[fname] = function
    return function
