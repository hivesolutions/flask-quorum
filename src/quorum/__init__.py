#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (C) 2008-2014 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from . import acl
from . import amazon
from . import base
from . import config
from . import daemon
from . import defines
from . import errors
from . import exceptions
from . import execution
from . import export
from . import extras
from . import formats
from . import http
from . import info
from . import jsonf
from . import legacy
from . import log
from . import mail
from . import meta
from . import model
from . import mongodb
from . import observer
from . import pusherc
from . import rabbitmq
from . import redisdb
from . import request
from . import route
from . import session
from . import structures
from . import template
from . import typesf
from . import unit_test
from . import util
from . import validation

from .acl import *
from .base import *
from .config import *
from .daemon import *
from .defines import *
from .errors import *
from .exceptions import *
from .execution import *
from .formats import *
from .http import *
from .info import *
from .jsonf import *
from .legacy import *
from .log import *
from .mail import *
from .meta import *
from .model import *
from .observer import *
from .structures import *
from .typesf import *
from .template import *
from .unit_test import *
from .util import *
from .validation import *

from .amazon import get_connection as get_amazon
from .amazon import get_bucket as get_amazon_bucket
from .amazon import clear_bucket as clear_amazon_bucket
from .amazon import get_key as get_amazon_key
from .amazon import exists_key as exists_amazon_key
from .amazon import delete_key as delete_amazon_key
from .execution import insert_work as run_back
from .execution import insert_work as run_background
from .mongodb import get_connection as get_mongo
from .mongodb import get_db as get_mongo_db
from .mongodb import drop_db as drop_mongo_db
from .mongodb import dumps as dumps_mongo
from .mongodb import object_id as object_id
from .pusherc import get_pusher as get_pusher
from .rabbitmq import get_connection as get_rabbit
from .rabbitmq import properties as properties_rabbit
from .redisdb import get_connection as get_redis
from .redisdb import dumps as dumps_redis
