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

from . import acl
from . import amazon
from . import amqp
from . import base
from . import config
from . import crypt
from . import daemon
from . import data
from . import defines
from . import errors
from . import exceptions
from . import execution
from . import export
from . import extras
from . import formats
from . import httpc
from . import jsonf
from . import legacy
from . import log
from . import mail
from . import meta
from . import model
from . import mongodb
from . import observer
from . import pusherc
from . import redisdb
from . import request
from . import route
from . import session
from . import storage
from . import structures
from . import template
from . import typesf
from . import unit_test
from . import util
from . import validation

from . import info as _info

from .acl import check_basic_auth, check_login, check_token, check_tokens, ensure_basic_auth,\
    ensure_login, ensure_user, ensure_session, ensure, ensure_auth, get_tokens_m, to_tokens_m
from .base import APP, RUN_CALLED, RUN_F, Quorum, monkey, call_run, run, prepare_app,\
    run_base, run_waitress, run_netius, load, unload, load_all, load_app_config,\
    load_paths, load_bundles, start_log, extra_logging, get_app, get_adapter, get_log,\
    get_level, get_handlers, get_handler, get_bundle, is_devel, finalize, before_request,\
    after_request, context_processor, start_execution, stop_execution, setup_models,\
    models_c, resolve, templates_path, bundles_path, base_path, has_context, ensure_context, onrun
from .config import conf, conf_prefix, conf_suffix, confs, confr, confd
from .crypt import Cipher, RC4, Spritz
from .daemon import Daemon
from .data import DataAdapter, MongoAdapter, TinyAdapter, Collection, MongoCollection, TinyCollection
from .defines import ITERABLES, MOBILE_REGEX, TABLET_REGEX, MOBILE_PREFIX_REGEX, BROWSER_INFO, OS_INFO,\
    WINDOWS_LOCALE
from .errors import errors_json
from .exceptions import BaseError, ServerInitError, ModuleNotFound, OperationalError, AssertionError,\
    NotFoundError, ValidationError, NotImplementedError, BaseInternalError, ValidationInternalError,\
    ValidationMultipleError, HTTPError, HTTPDataError, JSONError
from .execution import ExecutionThread, background, insert_work, interval_work,\
    seconds_work, minutes_work, hourly_work, daily_work, weekly_work, monthly_work,\
    seconds_eval, minutes_eval, hourly_eval, daily_eval, weekly_eval, monthly_eval
from .formats import xlsx_to_map
from .httpc import get_f, get, get_json, post_json, put_json, delete_json, HTTPResponse
from .info import NAME, VERSION, AUTHOR, EMAIL, DESCRIPTION, LICENSE, KEYWORDS, URL,\
    COPYRIGHT
from .jsonf import load_json
from .log import MemoryHandler, BaseFormatter, ThreadFormatter, rotating_handler, smtp_handler,\
    in_signature, has_exception, debug, info, warning, error, critical
from .mail import send_mail, send_mail_a
from .meta import Ordered
from .model import Model, LocalModel, Field, link, operation, view, field
from .mongodb import MongoMap, MongoEncoder
from .observer import Observable
from .structures import OrderedDict, LazyDict, LazyValue, lazy_dict, lazy
from .template import render_template, template_resolve
from .typesf import AbstractType, Type, File, Files, ImageFile, ImageFiles, image, images, Reference,\
    reference, References, references, Encrypted, encrypted, secure
from .unit_test import secured, TestCase
from .util import is_iterable, request_json, get_field, get_object, is_mobile, is_tablet,\
    is_browser, is_bot, browser_info, resolve_alias, page_types, find_types, norm_object, set_object,\
    leafs, load_form, load_locale, get_locale, get_langs, set_locale, reset_locale, anotate_async,\
    run_thread, camel_to_underscore, camel_to_readable, underscore_to_readable, generate_identifier,\
    to_locale, nl_to_br, nl_to_br_jinja, sp_to_nbsp, sp_to_nbsp_jinja, date_time, quote, unquote,\
    is_content_type, parse_content_type, verify, execute, JSONEncoder
from .validation import validate, validate_b, validate_e, safe, eq, gt, gte, lt, lte, not_null,\
    not_empty, not_false, is_in, is_lower, is_simple, is_email, is_url, is_regex, field_eq, field_gt,\
    field_gte, field_lt, field_lte, string_gt, string_lt, string_eq, equals, not_past, not_duplicate,\
    all_different, no_self

from .amazon import get_connection as get_amazon
from .amazon import get_bucket as get_amazon_bucket
from .amazon import clear_bucket as clear_amazon_bucket
from .amazon import get_key as get_amazon_key
from .amazon import exists_key as exists_amazon_key
from .amazon import delete_key as delete_amazon_key
from .amqp import get_connection as get_amqp
from .amqp import properties as properties_amqp
from .execution import insert_work as run_back
from .execution import insert_work as run_background
from .mongodb import get_connection as get_mongo
from .mongodb import reset_connection as reset_mongo
from .mongodb import get_db as get_mongo_db
from .mongodb import drop_db as drop_mongo_db
from .mongodb import object_id as object_id
from .mongodb import dumps as dumps_mongo
from .mongodb import serialize as serialize_mongo
from .mongodb import directions as directions_mongo
from .pusherc import get_pusher as get_pusher
from .redisdb import get_connection as get_redis
from .redisdb import dumps as dumps_redis
