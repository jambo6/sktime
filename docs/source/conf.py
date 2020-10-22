#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import os
import sys

import sktime

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# When we build the docs on readthedocs, we build the package and want to
# use the built files in order for sphinx to be able to properly read the
# Cython files. Hence, we do not add the source code path to the system
# path.
ON_READTHEDOCS = os.environ.get("READTHEDOCS") == "True"
if not ON_READTHEDOCS:
    sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
PROJECT = "sktime"
COPYRIGHT = "2019 - 2020 (BSD-3-Clause License)"
AUTHOR = "sktime developers"

# The full version, including alpha/beta/rc tags
CURRENT_VERSION = f"v{sktime.__version__}"

# If on readthedocs, and we're building the latest version, update tag to generate
# correct links in notebooks
if ON_READTHEDOCS:
    READTHEDOCS_VERSION = os.environ.get("READTHEDOCS_VERSION")
    if READTHEDOCS_VERSION == "latest":
        CURRENT_VERSION = "master"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.todo",
    "sphinx.ext.mathjax",
    # 'sphinx.ext.viewcode',  # link to auto-generated source code files (rst)
    "sphinx.ext.githubpages",
    "sphinx.ext.linkcode",  # link to GitHub source code via linkcode_resolve()
    "sphinx.ext.napoleon",
    "nbsphinx",  # integrates example notebooks
    "m2r2",  # markdown rendering
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", ".ipynb_checkpoints", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# see http://stackoverflow.com/q/12206334/562769
numpydoc_show_class_members = True
numpydoc_class_members_toctree = False

# generate autosummary even if no references
autosummary_generate = True
autodoc_default_flags = ["members", "inherited-members"]


def linkcode_resolve(domain, info):
    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/master/doc/source/conf.py#L286
        obj = sys.modules[info["module"]]
        for part in info["fullname"].split("."):
            obj = getattr(obj, part)
        import inspect
        import os

        fn = inspect.getsourcefile(obj)
        fn = os.path.relpath(fn, start=os.path.dirname(sktime.__file__))
        source, lineno = inspect.getsourcelines(obj)
        return fn, lineno, lineno + len(source) - 1

    if domain != "py" or not info["module"]:
        return None
    try:
        filename = "sktime/%s#L%d-L%d" % find_source()
    except Exception:
        filename = info["module"].replace(".", "/") + ".py"
    return "https://github.com/alan-turing-institute/sktime/blob/%s/%s" % (
        CURRENT_VERSION,
        filename,
    )


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"
# html_theme = 'bootstrap'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {
    "prev_next_buttons_location": None,
}

html_favicon = "images/sktime-favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

html_show_sourcelink = False

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "sktimedoc"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "sktime.tex", "sktime Documentation", "sktime developers", "manual"),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "sktime", "sktime Documentation", [AUTHOR], 1)]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "sktime",
        "sktime Documentation",
        AUTHOR,
        "sktime",
        "One line description of project.",
        "Miscellaneous",
    ),
]


def setup(app):
    def adds(pth):
        print("Adding stylesheet: %s" % pth)  # noqa: T001
        app.add_css_file(pth)

    adds("fields.css")  # for parameters, etc.


# -- Extension configuration -------------------------------------------------

# -- Options for nbsphinx extension ---------------------------------------
nbsphinx_execute = "always"  # whether or not to run notebooks
nbsphinx_allow_errors = False  # False
nbsphinx_timeout = 600  # time out in secs, set to -1 to disable timeout

# add Binder launch buttom at the top
CURRENT_FILE = "{{ env.doc2path( env.docname, base=None) }}"

# make sure Binder points to latest stable release, not master
BINDER_URL = f"https://mybinder.org/v2/gh/alan-turing-institute/sktime/{CURRENT_VERSION}?filepath={CURRENT_FILE}"  # noqa
nbsphinx_prolog = f"""
.. |binder| image:: https://mybinder.org/badge_logo.svg
.. _Binder: {BINDER_URL}
|Binder|_
"""

# add link to original notebook at the bottom
NOTEBOOK_URL = f"https://github.com/alan-turing-institute/sktime/tree/{CURRENT_VERSION}/{CURRENT_FILE}"  # noqa
nbsphinx_epilog = f"""
----
Generated by nbsphinx_. The Jupyter notebook can be found here_.
.. _here: {NOTEBOOK_URL}
.. _nbsphinx: https://nbsphinx.readthedocs.io/
"""

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"https://docs.python.org/": None}

# -- Options for _todo extension ----------------------------------------------
todo_include_todos = False