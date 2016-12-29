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

from . import common
from . import legacy

class BaseError(RuntimeError):
    """
    The base error class from which all the error
    classes should inherit, contains basic functionality
    to be inherited by all the "errors".
    """

    message = None
    """ The message value stored to describe the
    current error """

    def __init__(self, message):
        RuntimeError.__init__(self, message)
        self.message = message

class ServerInitError(BaseError):
    """
    The server initialization error that represents a
    problem in the boot process for the server, this
    error should not be raised during server runtime.
    """

    server = None
    """ The name (description) of the server that raised
    the initialization problem """

    def __init__(self, message, server = None):
        BaseError.__init__(self, message)
        self.server = server

class ModuleNotFound(BaseError):
    """
    The module not found error that represents a
    problem created by the failure to load a required module.
    This kind of error should be handled accordingly.
    """

    name = None
    """ The name (description) of the module that failed
    to load and raised the problem """

    def __init__(self, name):
        BaseError.__init__(self, "Failed to load '%s' module" % name)
        self.name = name

class OperationalError(BaseError):
    """
    The operational error class that should represent any
    error resulting from a business logic error.
    """

    code = 500
    """ The code to be used in the consequent serialization
    of the error in an HTTP response """

    def __init__(self, message, code = 500):
        BaseError.__init__(self, message)
        self.code = code

class AssertionError(OperationalError):
    """
    Error raised for failure to meet any pre-condition or
    assertion for a certain data set.
    """

    def __init__(self, message, code = 400):
        OperationalError.__init__(self, message, code = code)

class NotFoundError(OperationalError):
    """
    Error originated from an operation that was not able
    to be performed because it was not able to found the
    requested entity/value as defined by specification.
    """

    def __init__(self, message, code = 404):
        OperationalError.__init__(self, message, code = code)

class ValidationError(OperationalError):
    """
    Error raised when a validation on the model fails
    the error should associate a name in the model with
    a message describing the validation failure.
    """

    errors = None
    """ The map containing an association between the name
    of a field and a list of validation errors for it """

    model = None
    """ The model containing the values in it after the
    process of validation has completed """

    def __init__(self, errors, model):
        OperationalError.__init__(self, "Validation of submitted data failed", 400)
        self.errors = errors
        self.model = model

    def errors_s(self, encoding = "utf-8"):
        if not self.errors: return ""
        buffer = []
        is_first = True
        for name, errors in legacy.iteritems(self.errors):
            for error in errors:
                is_bytes = legacy.is_bytes(error)
                if is_bytes: error = error.decode(encoding)
                if is_first: is_first = False
                else: buffer.append(", ")
                buffer.append(name)
                buffer.append(" => ")
                buffer.append(error)
        return legacy.u("").join(buffer)

class NotImplementedError(OperationalError):
    """
    Error to be raised when a certain feature or route is not
    yet implemented or is not meant to be implemented at the
    defined abstraction level.
    """

    def __init__(self, message, code = 501):
        OperationalError.__init__(self, message, code = code)

class BaseInternalError(RuntimeError):
    """
    The base error class from which all the error
    classes should inherit, contains basic functionality
    to be inherited by all the internal "errors".
    """

    message = None
    """ The message value stored to describe the
    current error """

    def __init__(self, message):
        RuntimeError.__init__(self, message)
        self.message = message

class ValidationInternalError(BaseInternalError):
    """
    Error raised when a validation on the model fails
    the error should associate a name in the model with
    a message describing the validation failure.
    """

    name = None
    """ The name of the attribute that failed
    the validation """

    def __init__(self, name, message):
        BaseInternalError.__init__(self, message)
        self.name = name

class ValidationMultipleError(ValidationInternalError):
    """
    Exception/error considered to be equivalent to the
    validation internal error, with the exception that it
    may handle multiple errors at the same time.
    """

    errors = []
    """ The sequence containing the multiple errors associated
    with the validation multiple error """

    def __init__(self, name = None, message = None):
        ValidationInternalError.__init__(self, name, message)
        self.errors = []

    def add_error(self, name, message):
        if not self.name: self.name = name
        if not self.message: self.message = message
        self.errors.append((name, message))

    def add_exception(self, exception):
        self.add_error(exception.name, exception.message)

class HTTPError(BaseError):
    """
    Error raised when an HTTP (client) related issue
    arises, most of the problems should occur during
    the communication between client and server.
    """

    def __init__(self, message):
        BaseError.__init__(self, message)

class HTTPDataError(HTTPError):
    """
    Specialized HTTP error for data based stream where both
    the error code and message are known.

    A special error attribute is used store the original error
    that gave origin to this exception.
    """

    error = None
    """ The reference to the original and internal
    HTTP error that is going to be used in the reading
    of the underlying internal buffer """

    _data = None
    """ The underlying/internal data attribute that is
    going to be used to cache the binary contents of the
    error associated with this exception (data) stream """

    def __init__(self, error, code = None, message = None, extended = None):
        message = message or "Problem in the HTTP request"
        if extended == None: extended = common.base().is_devel()
        if code: message = "[%d] %s" % (code, message)
        if extended:
            data = self.read(error = error)
            try: data = data.decode("utf-8")
            except: data = legacy.str(data)
            if data: message += "\n" + data
        HTTPError.__init__(self, message)
        self.code = code
        self.error = error

class JSONError(HTTPError):
    """
    Error raised when a JSON based HTTP communication
    fails or is not accepted by the server pear.
    """

    data = None
    """ The deserialized version of the response information
    provided by the json request  """

    def __init__(self, data):
        HTTPError.__init__(self, "Problem requesting json data")
        self.data = data

    def __str__(self):
        exception_s = HTTPError.__str__(self)
        if not self.data: exception_s
        exception = self.data.get("exception", {})
        return exception.get("message", exception_s)

    def get_data(self):
        return self.data
