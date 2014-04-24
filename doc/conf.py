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

import os
import sys

# retrieves the current directory name from
# the current file, this is going to be used
# in the inclusion of new directories in the path
current_dir = os.path.dirname(__file__)

# sets the base source directory in the current
# system path variable so that linking to code
# documentation is possible
root_dir = current_dir + "/.."
root_dir = os.path.abspath(root_dir)
sys.path.append(root_dir)

# sets the base source directory in the current
# system path variable so that linking to code
# documentation is possible
src_dir = current_dir + "/../src"
src_dir = os.path.abspath(src_dir)
sys.path.append(src_dir)

# creates the reference to the quorum directory
# and then adds it to the current system path so
# that file under that directory are found
quorum_dir = os.path.join(src_dir, "quorum")
sys.path.append(quorum_dir)

# adds the themes path to the current python path
# to able to use third-party themes
themes_dir = current_dir + "/_themes"
themes_dir = os.path.abspath(themes_dir)
sys.path.append(themes_dir)

# verifies if the current environment is a read
# the docs (cloud infra-structure) one
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

import info

extensions = ["sphinx.ext.autodoc"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = info.NAME
copyright = info.COPYRIGHT
version = info.VERSION
release = info.VERSION
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
        info.NAME + ".tex",
        info.NAME + " documentation",
        info.AUTHOR,
        "manual"
    )
]
man_pages = [
    (
        "index",
        info.NAME,
        info.NAME + " documentation",
        [info.AUTHOR],
        1
    )
]
texinfo_documents = [(
    "index",
    info.NAME,
    info.NAME + " documentation",
    info.AUTHOR,
    info.NAME,
    info.DESCRIPTION,
    "Miscellaneous"
)]
