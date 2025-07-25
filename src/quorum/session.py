#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Flask Quorum
# Copyright (c) 2008-2025 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2025 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import uuid
import flask
import pickle
import datetime

import werkzeug.datastructures

from . import redisdb


class RedisSession(werkzeug.datastructures.CallbackDict, flask.sessions.SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True

        werkzeug.datastructures.CallbackDict.__init__(self, initial, on_update)

        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(flask.sessions.SessionInterface):

    serializer = pickle
    """ The serializer to be used for the values
    contained in the session (used on top of the class) """

    session_class = RedisSession
    """ The class to be used to encapsulate a session
    the generated object will be serialized """

    def __init__(self, _redis=None, prefix="session:", url=None):
        if _redis == None:
            _redis = redisdb._get_connection(url)

        self.redis = _redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid.uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return datetime.timedelta(days=1)

    def get_seconds(self, delta):
        return (
            delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10**6
        ) / 10**6

    def open_session(self, app, request):
        # tries to retrieve the session identifier from the
        # application cookie (or from parameters) in case
        # none is found generates a new one using the default
        # strategy and returns a new session object with that
        # session identifier
        sid = request.args.get("sid", request.args.get("session_id"))
        sid = sid or request.form.get("sid", request.form.get("session_id"))
        sid = sid or request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid)

        # tries to retrieve the session value from Redis in
        # case the values is successfully found loads it using
        # the serializer and returns the session object
        value = self.redis.get(self.prefix + sid)
        if not value == None:
            data = self.serializer.loads(value)
            return self.session_class(data, sid=sid)

        # returns a new session object with an already existing
        # session identifier, but not found in data source (Redis)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        # retrieves the domain associated with the cookie to
        # be able to correctly modify it
        domain = self.get_cookie_domain(app)

        # in case the session is no longer valid must delete
        # the reference in the Redis object and delete the cookie
        # from the current response object
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            return

        # retrieves the Redis expiration date from the provided
        # session object and the expiration value for the cookie
        # and then serializes the dictionary version of the session
        # so that it may be set as a string value in Redis
        redis_expire = self.get_redis_expiration_time(app, session)
        cookie_expire = self.get_expiration_time(app, session)
        value = self.serializer.dumps(dict(session))
        total_seconds = self.get_seconds(redis_expire)
        self.redis.setex(
            self.prefix + session.sid, value=value, time=int(total_seconds)
        )

        # sets the proper cookie value (with session identifier) in the
        # response object so that the client may be able to re-use the
        # session object latter for operations
        response.set_cookie(
            app.session_cookie_name,
            session.sid,
            expires=cookie_expire,
            httponly=True,
            domain=domain,
        )
