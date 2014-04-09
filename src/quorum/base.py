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

import werkzeug.debug

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
import template
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

ESCAPE_EXTENSIONS = (
    ".xml",
    ".html",
    ".xhtml",
    ".xml.tpl",
    ".html.tpl",
    ".xhtml.tpl"
)
""" The sequence containing the various extensions
for which the autoescape mode will be enabled  by
default as expected by the end developer """

class Quorum(flask.Flask):
    """
    The top level application class that inherits from the
    flask based one. Should be responsible for the implementation
    of some of the modifications to the original application
    object infra-structure.
    """

    def select_jinja_autoescape(self, filename):
        if filename == None: return False
        if filename.endswith(ESCAPE_EXTENSIONS): return True
        return self.select_jinja_autoescape(self, filename)

def monkey():
    """
    Runs the dirty job of monkey patching the flask module
    so that some of its functions get redirected to new
    quorum functions that add extra behavior.

    This is an internal function and should be changed only
    when handling the internals of the quorum framework.
    """

    flask._render_template = flask.render_template
    flask.render_template = template.render_template

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

def prepare_app():
    """
    Prepares the global application object encapsulating
    it with the proper decorators so that it is enabled
    with the proper features (eg: debugging capabilities).

    This method should be called and the returned application
    object used instead of the global one.

    @rtype: Application
    @return: The decorated application object with the proper
    capabilities enabled, this object should be used for the
    serving operations instead of the global one.
    """

    app = APP
    if app.debug: app = werkzeug.debug.DebuggedApplication(app, True)
    return app

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

    # prepares the application object so that it becomes ready
    # to be executed by the server in the proper way
    app = prepare_app()

    # starts the serving process for the waitress server with
    # the proper network configuration values, note that no ssl
    # support is currently available for waitress
    waitress.serve(
        app,
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
    kwargs["handlers"] = get_handlers()
    kwargs["level"] = get_level()

    # prepares the application object so that it becomes ready
    # to be executed by the server in the proper way
    app = prepare_app()

    # creates the netius wsgi server reference using the provided
    # application object and the constructed keyword arguments
    # and then call the serve method starting the event loop with
    # the proper network configuration
    server = netius.servers.WSGIServer(app, **kwargs)
    server.serve(
        host = host,
        port = port,
        ssl = ssl,
        key_file = key_file,
        cer_file = cer_file
    )

def load(
    app = None,
    name = None,
    locales = ("en_us",),
    secret_key = None,
    execution = True,
    redis_session = False,
    mongo_database = None,
    logger = None,
    models = None,
    safe = False,
    **kwargs
):
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
    :type locales: List
    :param locales: The list containing the various locale strings for\
    the locales available for the application to be loaded.
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
    :type safe: bool
    :param safe: If the application should be run in a safe mode meaning that\
    extra validations will be done to ensure proper execution, typically these\
    kind of validations have a performance impacts (not recommended).
    :rtype: Application
    :return: The application that is used by the loaded quorum environment in\
    case one was provided that is retrieved, otherwise the newly created one is\
    returned instead.
    """

    global APP
    if APP: return APP

    # runs the initial loading of the configuration from all
    # the currently available sources (eg: file, environment, etc.)
    load_all()

    # retrieves the value of all the configuration considered
    # to be base and that are going to be used in the loading
    # of the current application (with default values)
    debug = config.conf("DEBUG", False, cast = bool)
    reloader = config.conf("RELOADER", False, cast = bool)
    level_s = config.conf("LEVEL", "WARNING")
    name = config.conf("NAME", name)
    instance = config.conf("INSTANCE", None)
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

    # creates the proper values according to the currently provided
    # ones so that they match the ones that are expected
    name = name + "-" + instance if instance else name
    prefix = instance + "-" if instance else ""
    suffix = "-" + instance if instance else ""
    level = logging.DEBUG if debug else logging.getLevelName(level_s)
    logger = logger and prefix + logger

    # retrieves the last stack element as the previous element and
    # uses it to retrieve the module that has triggered the loading
    previous = inspect.stack()[1]
    module = inspect.getmodule(previous[0])

    # uses the module to retrieve the base path for the execution of
    # the app, this is going to be used to calculate relative paths
    path = os.path.dirname(module.__file__)

    # creates the initial app reference using the provided one or
    # creates a new one from the provided/computed name
    app = app or Quorum(name)

    # loads the app configuration from the provided keyword arguments
    # map and then starts the logging process with the requested logger
    # and with the provided "verbosity" level
    load_app_config(app, kwargs)
    start_log(app, name = logger, level = level)

    # loads the various paths associated with the application into the
    # current environment to reduce the amount of issues related with
    # the importing of modules and other resources
    load_paths(app)

    # loads the complete set of bundle localized in the proper path into
    # the current app environment, this is a blocking operation and may
    # take some time to be performed completely
    load_bundles(app)

    # sets the various eval context filters as such by setting their eval
    # context filter flag to true the jinja infra-structure will handle
    # the rest of the operations so that it's properly used
    util.nl_to_br_jinja.evalcontextfilter = True

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
    if mongo_database: mongodb.database = mongo_database + suffix
    if models: setup_models(models)
    if force_ssl: extras.SSLify(app)
    app.before_request(before_request)
    app.after_request(after_request)
    app.context_processor(context_processor)
    app.template_filter("locale")(util.to_locale)
    app.template_filter("nl_to_br")(util.nl_to_br_jinja)
    app.request_class = request.Request
    app.locales = locales
    app.safe = safe
    app.debug = debug
    app.use_debugger = debug
    app.use_reloader = reloader
    app.models = models
    app.module = module
    app.path = path
    app.secret_key = secret_key
    app.old_route = app.route
    app.route = route.route
    app.jinja_options = dict(
        finalize = finalize
    )
    APP = app

    # verifies if the module that has called the method is not
    # of type main and in case it's not calls the runner methods
    # immediately so that the proper initialization is done, then
    # returns the app reference object to the caller method
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

def load_paths(app):
    if not app.root_path in sys.path: sys.path.insert(0, app.root_path)

def load_bundles(app, offset = 2):
    # creates the base dictionary that will handle all the loaded
    # bundle information and sets it in the current application
    # object reference so that may be used latter on
    bundles = dict()
    app.bundles = bundles

    # inspects the current stack to obtain the reference to the base
    # application module and then uses it to calculate the base path
    # for the application, from there re-constructs the path to the
    # bundle file and verifies its own existence
    element = inspect.stack()[offset]
    module = inspect.getmodule(element[0])
    base_folder = os.path.dirname(module.__file__)
    bundles_path = os.path.join(base_folder, "bundles")
    if not os.path.exists(bundles_path): return

    # list the bundles directory files and iterates over each of the
    # files to load its own contents into the bundles "registry"
    paths = os.listdir(bundles_path)
    for path in paths:
        # joins the current (base) bundles path with the current path
        # in iteration to create the full path to the file and opens
        # it trying to read its json based contents
        path_f = os.path.join(bundles_path, path)
        file = open(path_f, "rb")
        try: data_j = json.load(file)
        except: continue
        finally: file.close()

        # unpacks the current path in iteration into the base name,
        # locale string and file extension to be used in the registration
        # of the data in the bundles registry
        try: _base, locale, _extension = path.split(".", 2)
        except: continue

        # retrieves a possible existing map for the current locale in the
        # registry and updates such map with the loaded data, then re-updates
        # the reference to the locale in the current bundle registry
        bundle = bundles.get(locale, {})
        bundle.update(data_j)
        bundles[locale] = bundle

def start_log(app, name = None, level = logging.WARN, format = LOGGING_FORMAT):
    # "resolves" the proper logger file path taking into account
    # the currently defined operative system, should uses the system
    # level path in case the operative system is unix based
    if os.name == "nt": path_t = "%s"
    else: path_t = "/var/log/%s"
    path = name and path_t % name

    # creates the map that is going to be used to store the
    # various handlers registered for the logger
    app.handlers = dict()

    # creates the formatter object from the provided string
    # so that it may be used in the various handlers
    formatter = logging.Formatter(format)

    # retrieves the reference to the logger object currently
    # associated with the app and disable the parent in it,
    # then removes the complete set of associated handlers and
    # sets the proper debug level, note that the logger is
    # going to be shared between quorum and flask (common logger)
    logger = app.logger if hasattr(app, "logger") else logging.getLogger("quorum")
    logger.parent = None
    logger.handlers = []
    logger.setLevel(level)

    # creates both the stream and the memory based handlers that
    # are going to be used for the current logger
    stream_handler = logging.StreamHandler()
    memory_handler = log.MemoryHandler()

    try:
        # tries to create the file handler for the logger with the
        # resolve path (operation may fail for permissions)
        file_handler = path and logging.FileHandler(path)
    except:
        # in case there's an error creating the file handler for
        # the logger prints an error message indicating the problem
        sys.stderr.write("Problem starting logging for file '%s'\n" % path)
        file_handler = None

    # adds the various created handler to the current logger so that
    # they are going to be used when using the logger for output
    if stream_handler: logger.addHandler(stream_handler)
    if memory_handler: logger.addHandler(memory_handler)
    if file_handler: logger.addHandler(file_handler)

    # for each of the handlers adds them to the handlers map in case
    # they are valid and defined (no problem in construction)
    if stream_handler: app.handlers["stream"] = stream_handler
    if memory_handler: app.handlers["memory"] = memory_handler
    if file_handler: app.handlers["file"] = file_handler

    # iterates over the complete set of handlers currently
    # registered in the logger to properly set the formatter
    # and the level for all of them (as specified)
    for handler in logger.handlers:
        handler.setFormatter(formatter)
        handler.setLevel(level)

    # sets the current logger in the top level app value so that
    # this logger is going to be used as the quorum logger
    app.logger_q = logger

def get_log(app = None):
    app = app or APP
    is_custom = hasattr(app, "logger_q")
    return app.logger_q if is_custom else app.logger

def get_level(app = None):
    logger = get_log(app = app)
    return logger.level

def get_handlers(app = None):
    logger = get_log(app = app)
    return logger.handlers

def get_bundle(name):
    return APP.bundles.get(name, None)

def finalize(value):
    # returns an empty string as value representation
    # for unset values, this is the default representation
    # to be used in the template engine
    if value == None: return ""
    return value

def before_request():
    flask.request.args_s = util.load_form(flask.request.args)
    flask.request.form_s = util.load_form(flask.request.form)
    flask.request.locale = util.load_locale(APP.locales)
    util.set_locale()

def after_request(response):
    if APP.safe: util.reset_locale()
    util.anotate_async(response)
    return response

def context_processor():
    return dict(
        acl = acl.check_login,
        conf = config.conf,
        locale = util.to_locale,
        nl_to_br = util.nl_to_br,
        date_time = util.date_time
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
    _models_c = models_c(models = models)
    for model_c in _models_c: model_c.setup()

def models_c(models = None):
    # retrieves the proper models defaulting to the current
    # application models in case they are not defined
    models = models or APP.models

    # creates the list that will hold the various model
    # class discovered through module analysis
    models_c = []

    # iterates over the complete set of items in the models
    # modules to find the ones that inherit from the base
    # model class for those are the real models
    for _name, value in models.__dict__.iteritems():
        # verifies if the current value in iteration inherits
        # from the top level model in case it does not continues
        # the loop as there's nothing to be done
        try: is_valid = issubclass(value, model.Model)
        except: is_valid = False
        if not is_valid: continue

        # adds the current value in iteration as a new class
        # to the list that hold the various model classes
        models_c.append(value)

    # returns the list containing the various model classes
    # to the caller method as expected by definition
    return models_c

def resolve(identifier = "_id"):
    # creates the list that will hold the definition of the current
    # model classes with a sequence of name and identifier values
    entities = []

    # retrieves the complete set of model classes registered
    # for the current application and for each of them retrieves
    # the name of it and creates a tuple with the name and the
    # identifier attribute name adding then the tuple to the
    # list of entities tuples (resolution list)
    _models_c = models_c()
    for model_c in _models_c:
        name = model_c._name()
        tuple = (name, identifier)
        entities.append(tuple)

    # returns the resolution list to the caller method as requested
    # by the call to this method
    return entities

def templates_path():
    return os.path.join(APP.root_path, APP.template_folder)

def bundles_path():
    return os.path.join(APP.root_path, "bundles")

def base_path(*args, **kwargs):
    return os.path.join(APP.root_path, *args)

def onrun(function):
    fname = function.__name__
    if fname in RUN_F: return
    RUN_F[fname] = function
    return function

# runs the monkey patching of the flask module so that it
# may be used according to the quorum specification, this
# is used in order to avoid minimal effort in the conversion
# of old flask based applications (reverse compatibility)
monkey()
