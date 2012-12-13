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

import util
import mongodb
import validation
import exceptions

class Model(object):

    def __init__(self, model = None):
        self.__dict__["model"] = model or {}

    def __getattr__(self, name):
        return self.model[name]

    def __setattr__(self, name, value):
        is_base = name in self.__dict__
        if is_base: self.__dict__[name] = value
        else: self.model[name] = value

    @classmethod
    def new(cls, model = None, build = False):
        instance = cls()
        instance.apply(model)
        build and instance.build(instance.model, False)
        return instance

    @classmethod
    def get(cls, *args, **kwargs):
        map, build, raise_e = cls._get_attrs(kwargs, (
            ("map", False),
            ("build", True),
            ("raise_e", True)
        ))

        collection = cls._collection()
        model = collection.find_one(kwargs)
        if not model and raise_e: raise RuntimeError("%s not found" % cls.__name__)
        if not model and not raise_e: return model
        build and cls.build(model, map)
        return model if map else cls.new(model = model)

    @classmethod
    def find(cls, *args, **kwargs):
        map, build = cls._get_attrs(kwargs, (
            ("map", False),
            ("build", True)
        ))

        collection = cls._collection()
        models = [model for model in collection.find(kwargs)]
        build and [cls.build(model, map) for model in models]
        models = models if map else [cls.new(model = model) for model in models]
        return models

    @classmethod
    def build(cls, model, map):
        pass

    @classmethod
    def _collection(cls):
        name = cls._name()
        db = mongodb.get_db()
        collection = db[name]
        return collection

    @classmethod
    def _name(cls):
        # retrieves the class object for the current instance and then
        # converts it into lower case value in order to serve as the
        # name of the collection to be used
        name = cls.__name__.lower()
        return name

    @classmethod
    def _get_attrs(cls, kwargs, attrs):
        _attrs = []

        for attr, value in attrs:
            if not attr in kwargs:
                _attrs.append(value)
                continue

            value = kwargs[attr]
            del kwargs[attr]
            _attrs.append(value)

        return _attrs

    def val(self, name, default = None):
        return self.model.get(name, default)

    def apply(self, model = None):
        self.model = model or util.get_object()

    def is_new(self):
        return not "_id" in self.model

    def save(self):
        # runs the validation process in the current model, this
        # should ensure that the model is ready to be saved in the
        # data source, without corruption of it
        self._validate()

        # retrieves the reference to the store object to be used and
        # uses it to store the current model data
        store = self._get_store()
        store.save(self.model)

    def validate(self):
        return []

    def validate_new(self):
        return self.validate()

    def dumps(self):
        return mongodb.dumps(self.model)

    def _get_store(self):
        return  self.__class__._collection()

    def _validate(self):
        # checks if the current model is new (create operation)
        # and sets the proper validation methods retrieval method
        is_new = self.is_new()
        if is_new: method = self.validate_new
        else: method = self.validate

        # runs the validation process on the various arguments
        # provided to the account and in case an error is returned
        # raises a validation error to the upper layers
        errors, object = validation.validate(
            method,
            object = self.model,
            build = False
        )
        if errors: raise exceptions.ValidationError(errors, object)
