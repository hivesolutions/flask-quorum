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

import os
import sys

# sets the base source directory in the current
# system path variable so that linking to code
# documentation is possible
current_dir = os.path.dirname(__file__)
src_dir = current_dir + "/../src"
src_dir = os.path.abspath(src_dir)
sys.path.append(src_dir)

# adds the themes path to the current python path
# to able to use third-party themes
themes_dir = current_dir + "/_themes"
themes_dir = os.path.abspath(themes_dir)
sys.path.append(themes_dir)

# verifies if the current environment is a read
# the docs (cloud infra-structure) one
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

extensions = ["sphinx.ext.autodoc"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = u"Quorum"
copyright = u"2013, Hive Solutions Lda."
version = "0.1.0"
release = "0.1.0"
exclude_patterns = ["_build"]
pygments_style = "sphinx"
html_theme = "kr"
html_theme_path = ["_themes"]
html_static_path = ["_static"]
htmlhelp_basename = "quorumdoc"
latex_elements = {}
latex_documents = [
    (
        "index",
        "Quorum.tex",
        u"Quorum Documentation",
        u"Hive Solutions Lda.",
        "manual"
    )
]
man_pages = [
    (
        "index",
        "quorum",
        u"Quorum Documentation",
        [u"Hive Solutions Lda."],
        1
    )
]
texinfo_documents = [(
    "index",
    "Quorum",
    u"Quorum Documentation",
    u"Hive Solutions Lda.",
    "Quorum",
    "An extension to flask for, ssl, acl, etc.",
    "Miscellaneous"
)]
