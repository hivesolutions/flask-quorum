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
import flask

import base

def render_template(template_name_or_list, **context):
    # runs the resolution process in the provided template name
    # so that the proper name is going to be used when rendering
    # the template, then retrieves the underlying flask render
    # template function and calls it with the new resolved name
    template_name_or_list = template_resolve(template_name_or_list)
    render_template = getattr(flask, "_render_template")
    return render_template(template_name_or_list, **context)

def template_resolve(template):
    """
    Resolves the provided template path, using the currently
    defined locale. It tries to find the best match for the
    template file falling back to the default (provided) template
    path in case the best one could not be found.

    @type template: String
    @param template: Path to the template file that is going to
    be "resolved" trying to find the best locale match.
    @rtype: String
    @return: The resolved version of the template file taking into
    account the existence or not of the best locale template.
    """

    # splits the provided template name into the base and the name values
    # and then splits the name into the base file name and the extension
    # part so that it's possible to re-construct the name with the proper
    # locale naming part included in the name
    fbase, name = os.path.split(template)
    fname, extension = name.split(".", 1)

    # creates the base file name for the target (locale based) template
    # and then joins the file name with the proper base path to create
    # the "full" target file name
    target = fname + "." + flask.request.locale + "." + extension
    target = fbase + "/" + target if fbase else target

    # sets the fallback name as the "original" template path, because
    # that's the default and expected behavior for the template engine
    fallback = template

    # retrieves the base templates path from the base infra-structure this
    # is going to be used in the resolution of the complete template file
    # file in order to verify existence of the file
    templates_path = base.templates_path()

    # "joins" the target path and the templates (base) path to create
    # the fill path to the target template, then verifies if it exists
    # and in case it does sets it as the template name otherwise uses
    # the fallback value as the target template path
    target_f = os.path.join(templates_path, target)
    template = target if os.path.exists(target_f) else fallback
    return template
