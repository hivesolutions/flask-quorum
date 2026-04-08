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

import os
import logging
import tempfile
import unittest

import logging.handlers

import quorum

from quorum import log


class LogTest(quorum.TestCase):

    @quorum.secured
    def test_silent_value(self):
        self.assertEqual(quorum.SILENT, logging.CRITICAL + 1)
        self.assertEqual(type(quorum.SILENT), int)

    @quorum.secured
    def test_silent_above_critical(self):
        self.assertTrue(quorum.SILENT > logging.CRITICAL)

    @quorum.secured
    def test_trace_value(self):
        self.assertEqual(quorum.TRACE, 5)
        self.assertEqual(quorum.TRACE, logging.DEBUG - 5)
        self.assertEqual(type(quorum.TRACE), int)

    @quorum.secured
    def test_trace_below_debug(self):
        self.assertTrue(quorum.TRACE < logging.DEBUG)

    @quorum.secured
    def test_level_ordering(self):
        self.assertTrue(quorum.TRACE < logging.DEBUG)
        self.assertTrue(logging.DEBUG < logging.INFO)
        self.assertTrue(logging.INFO < logging.WARNING)
        self.assertTrue(logging.WARNING < logging.ERROR)
        self.assertTrue(logging.ERROR < logging.CRITICAL)
        self.assertTrue(logging.CRITICAL < quorum.SILENT)

    @quorum.secured
    def test_rotating_handler(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        try:
            handler = quorum.rotating_handler(path=path, max_bytes=1024, max_log=3)

            self.assertEqual(type(handler), logging.handlers.RotatingFileHandler)
            self.assertEqual(handler.maxBytes, 1024)
            self.assertEqual(handler.backupCount, 3)

            handler.close()
        finally:
            os.unlink(path)

    @quorum.secured
    def test_rotating_handler_defaults(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        try:
            handler = quorum.rotating_handler(path=path)

            self.assertEqual(handler.maxBytes, 1048576)
            self.assertEqual(handler.backupCount, 5)

            handler.close()
        finally:
            os.unlink(path)

    @quorum.secured
    def test_patch_logging(self):
        quorum.patch_logging()

        result = logging.getLevelName(quorum.TRACE)

        self.assertEqual(result, "TRACE")

    @quorum.secured
    def test_patch_logging_reverse(self):
        quorum.patch_logging()

        result = logging.getLevelName("TRACE")

        self.assertEqual(result, quorum.TRACE)

    @quorum.secured
    def test_patch_logging_idempotent(self):
        quorum.patch_logging()
        quorum.patch_logging()

        result = logging.getLevelName(quorum.TRACE)

        self.assertEqual(result, "TRACE")

    @quorum.secured
    def test_patch_logging_logger_trace(self):
        quorum.patch_logging()

        logger = logging.getLogger("quorum.test.trace")

        self.assertTrue(hasattr(logger, "trace"))
        self.assertTrue(callable(logger.trace))

    @quorum.secured
    def test_patch_logging_logger_trace_call(self):
        quorum.patch_logging()

        logger = logging.getLogger("quorum.test.trace.call")
        logger.setLevel(quorum.TRACE)
        records = []
        handler = logging.Handler()
        handler.setLevel(quorum.TRACE)
        handler.emit = lambda record: records.append(record)
        logger.addHandler(handler)

        try:
            logger.trace("trace test message")

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].getMessage(), "trace test message")
            self.assertEqual(records[0].levelno, quorum.TRACE)
            self.assertEqual(records[0].levelname, "TRACE")
        finally:
            logger.removeHandler(handler)

    @quorum.secured
    def test_patch_logging_logger_trace_filtered(self):
        quorum.patch_logging()

        logger = logging.getLogger("quorum.test.trace.filtered")
        logger.setLevel(logging.DEBUG)
        records = []
        handler = logging.Handler()
        handler.setLevel(quorum.TRACE)
        handler.emit = lambda record: records.append(record)
        logger.addHandler(handler)

        try:
            # the trace message should be filtered since the logger
            # level is set to DEBUG which is above TRACE
            logger.trace("this should be filtered")

            self.assertEqual(len(records), 0)
        finally:
            logger.removeHandler(handler)

    @quorum.secured
    def test_level_trace_before_patch(self):
        # temporarily removes the patched state to simulate a
        # scenario where patch_logging() has not been called yet
        patched = getattr(logging, "_quorum_patched", None)
        if patched:
            del logging._quorum_patched
        trace_method = getattr(logging.Logger, "trace", None)
        if trace_method:
            del logging.Logger.trace
        try:
            result = quorum._level("TRACE")

            self.assertEqual(result, quorum.TRACE)
            self.assertEqual(result, 5)
        finally:
            if patched:
                logging._quorum_patched = patched
            if trace_method:
                logging.Logger.trace = trace_method

    @quorum.secured
    def test_level_trace_after_patch(self):
        quorum.patch_logging()

        result = quorum._level("TRACE")

        self.assertEqual(result, quorum.TRACE)
        self.assertEqual(result, 5)

    @quorum.secured
    def test_level_silent(self):
        result = quorum._level("SILENT")

        self.assertEqual(result, quorum.SILENT)

    @quorum.secured
    def test_level_integer(self):
        result = quorum._level(logging.DEBUG)

        self.assertEqual(result, logging.DEBUG)

    @quorum.secured
    def test_level_none(self):
        result = quorum._level(None)

        self.assertEqual(result, None)

    @quorum.secured
    def test_in_signature(self):
        def sample(a, b, secure=None):
            pass

        result = log.in_signature(sample, "secure")

        self.assertEqual(result, True)

    @quorum.secured
    def test_in_signature_missing(self):
        def sample(a, b):
            pass

        result = log.in_signature(sample, "secure")

        self.assertEqual(result, False)

    @quorum.secured
    def test_in_signature_args(self):
        def sample(a, b, secure):
            pass

        result = log.in_signature(sample, "secure")

        self.assertEqual(result, True)

    @quorum.secured
    def test_memory_handler(self):
        memory_handler = quorum.MemoryHandler()
        formatter = logging.Formatter("%(message)s")
        memory_handler.setFormatter(formatter)

        latest = memory_handler.get_latest()
        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        record = logging.makeLogRecord(
            dict(msg="hello world", levelname=logging.getLevelName(logging.INFO))
        )
        memory_handler.emit(record)
        latest = memory_handler.get_latest()

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world"])

        record = logging.makeLogRecord(
            dict(msg="hello world 2", levelname=logging.getLevelName(logging.ERROR))
        )
        memory_handler.emit(record)
        latest = memory_handler.get_latest()

        self.assertEqual(len(latest), 2)
        self.assertEqual(latest, ["hello world 2", "hello world"])

        latest = memory_handler.get_latest(level=logging.ERROR)

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world 2"])

        latest = memory_handler.get_latest(level=logging.CRITICAL)

        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        latest = memory_handler.get_latest(level=logging.INFO)

        self.assertEqual(len(latest), 2)
        self.assertEqual(latest, ["hello world 2", "hello world"])

        latest = memory_handler.get_latest(count=1, level=logging.INFO)

        self.assertEqual(len(latest), 1)
        self.assertEqual(latest, ["hello world 2"])

    @quorum.secured
    def test_memory_handler_file(self):
        memory_handler = quorum.MemoryHandler()
        formatter = logging.Formatter("%(message)s")
        memory_handler.setFormatter(formatter)

        latest = memory_handler.get_latest()
        self.assertEqual(len(latest), 0)
        self.assertEqual(latest, [])

        record = logging.makeLogRecord(
            dict(msg="hello world", levelname=logging.getLevelName(logging.INFO))
        )
        memory_handler.emit(record)
        record = logging.makeLogRecord(
            dict(msg="hello world 2", levelname=logging.getLevelName(logging.INFO))
        )
        memory_handler.emit(record)

        file = quorum.legacy.BytesIO()

        memory_handler.flush_to_file(file, clear=False)

        file.seek(0)
        contents = file.read()

        self.assertEqual(contents, b"hello world\nhello world 2\n")

        file = quorum.legacy.BytesIO()

        memory_handler.flush_to_file(file, reverse=False)

        file.seek(0)
        contents = file.read()

        self.assertEqual(contents, b"hello world 2\nhello world\n")

        latest = memory_handler.get_latest(count=1)
        self.assertEqual(len(latest), 0)
