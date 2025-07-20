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

import calendar
import datetime

import quorum


class ExecutionTest(quorum.TestCase):

    @quorum.secured
    def test_seconds_eval(self):
        now = datetime.datetime(year=2014, month=1, day=1, second=0)
        result = quorum.seconds_eval(1, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=1, second=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=1, second=59)
        result = quorum.seconds_eval(1, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=1, minute=1, second=0)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

    @quorum.secured
    def test_daily_eval(self):
        now = datetime.datetime(year=2014, month=1, day=1)
        result = quorum.daily_eval(0, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=2)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2013, month=12, day=31)
        result = quorum.daily_eval(0, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2013, month=12, day=31, hour=1)
        result = quorum.daily_eval(0, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2013, month=12, day=31, hour=1)
        result = quorum.daily_eval(3600, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=1, hour=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

    @quorum.secured
    def test_weekly_eval(self):
        now = datetime.datetime(year=2014, month=1, day=1)
        result = quorum.weekly_eval(4, 0, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=3)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=6)
        result = quorum.weekly_eval(4, 0, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=10)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=10, hour=1)
        result = quorum.weekly_eval(4, 3600, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=10, hour=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=10, hour=3)
        result = quorum.weekly_eval(4, 3600, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=17, hour=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=11, hour=3)
        result = quorum.weekly_eval(4, 3600, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=17, hour=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

    @quorum.secured
    def test_monthly_eval(self):
        now = datetime.datetime(year=2014, month=1, day=1)
        result = quorum.monthly_eval(6, 0, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=6)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=6)
        result = quorum.monthly_eval(6, 0, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=6)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=6, hour=1)
        result = quorum.monthly_eval(6, 0, now=now)
        expected_d = datetime.datetime(year=2014, month=2, day=6)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=6, hour=1)
        result = quorum.monthly_eval(6, 3600, now=now)
        expected_d = datetime.datetime(year=2014, month=1, day=6, hour=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

        now = datetime.datetime(year=2014, month=1, day=6, hour=2)
        result = quorum.monthly_eval(6, 3600, now=now)
        expected_d = datetime.datetime(year=2014, month=2, day=6, hour=1)
        expected_t = calendar.timegm(expected_d.utctimetuple())
        self.assertEqual(result, expected_t)

    @quorum.secured
    def test_insert_work_description(self):
        thread = quorum.ExecutionThread()

        def dummy():
            pass

        thread.insert_work(dummy, description="dummy-work")
        self.assertEqual(len(thread.work_list), 1)

        _time, callable_o, _callback, _args, _kwargs, description = thread.peek_work()
        self.assertEqual(description, "dummy-work")

    @quorum.secured
    def test_interval_work_description(self):
        calls = []

        def dummy():
            calls.append(True)

        recorded = []

        def custom_insert_work(
            callable_o,
            args=[],
            kwargs={},
            target_time=None,
            callback=None,
            description=None,
        ):
            recorded.append((callable_o, target_time, callback, description))

        original_insert_work = quorum.execution.insert_work
        quorum.execution.insert_work = custom_insert_work

        try:
            result = quorum.interval_work(
                dummy,
                initial=10,
                interval=5,
                eval=lambda: 20,
                description="dummy-work",
            )

            self.assertEqual(result, 10)
            self.assertEqual(len(recorded), 1)
            callable_o, target_time, _callback, description = recorded[0]
            self.assertEqual(target_time, 10)
            self.assertEqual(description, "dummy-work")

            del recorded[:]
            callable_o()

            self.assertEqual(len(recorded), 1)
            _callable_o, target_time, _callback, description = recorded[0]
            self.assertEqual(target_time, 20)
            self.assertEqual(description, "dummy-work")
        finally:
            quorum.execution.insert_work = original_insert_work
