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

    def __getattribute__(self, name):
        try:
            model = object.__getattribute__(self, "model")
            if name in model: return model[name]
        except AttributeError: pass
        return object.__getattribute__(self, name)

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
        cls.types(model)
        build and cls.build(model, map)
        return cls.types(model) if map else cls.new(model = model)

    @classmethod
    def find(cls, *args, **kwargs):
        map, build = cls._get_attrs(kwargs, (
            ("map", False),
            ("build", True)
        ))

        collection = cls._collection()
        models = [cls.types(model) for model in collection.find(kwargs)]
        build and [cls.build(model, map) for model in models]
        models = models if map else [cls.new(model = model) for model in models]
        return models

    @classmethod
    def definition(cls, name):
        return getattr(cls, name) if hasattr(cls, name) else {}

    @classmethod
    def validate(cls):
        return []

    @classmethod
    def validate_new(cls):
        return cls.validate()

    @classmethod
    def build(cls, model, map):
        cls.rules(model, map)
        cls._build(model, map)

    @classmethod
    def rules(cls, model, map):
        for name, _value in model.items():
            definition = cls.definition(name)
            is_private = definition.get("private", False)
            if not is_private: continue
            del model[name]

    @classmethod
    def types(cls, model):
        for name, value in model.items():
            definition = cls.definition(name)
            _type = definition.get("type", str)
            model[name] = _type(value)

        return model

    @classmethod
    def _build(cls, model, map):
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
        cls = self.__class__
        cls.types(self.model)

    def is_new(self):
        return not "_id" in self.model

    def save(self):
        # filters the values that are present in the current
        # model so that only those are stored in
        model = self._filter()

        # runs the validation process in the current model, this
        # should ensure that the model is ready to be saved in the
        # data source, without corruption of it
        self._validate(model = model)

        # retrieves the reference to the store object to be used and
        # uses it to store the current model data
        store = self._get_store()
        store.save(model)

    def dumps(self):
        return mongodb.dumps(self.model)

    def _get_store(self):
        return  self.__class__._collection()

    def _validate(self, model = None):
        # starts the model reference with the current model in
        # case none is defined
        model = model or self.model

        # retrieves the class associated with the current instance
        # to be able to retrieve the correct validate methods
        cls = self.__class__

        # checks if the current model is new (create operation)
        # and sets the proper validation methods retrieval method
        is_new = self.is_new()
        if is_new: method = cls.validate_new
        else: method = cls.validate

        # runs the validation process on the various arguments
        # provided to the account and in case an error is returned
        # raises a validation error to the upper layers
        errors, object = validation.validate(
            method,
            object = model,
            build = False
        )
        if errors: raise exceptions.ValidationError(errors, object)

    def _filter(self):
        # creates the model that will hold the "filtered" model
        # with all the items that conform with the class specification
        model = {}

        # retrieves the class associated with the current instance
        # to be able to retrieve the correct definition methods
        cls = self.__class__

        # iterates over all the model items to filter the ones
        # that are not valid for the current class context
        for name, value in self.model.items():
            if not hasattr(cls, name): continue
            model[name] = value

        # returns the model containing the "filtered" items resulting
        # from the validation of the items against the model class
        return model
