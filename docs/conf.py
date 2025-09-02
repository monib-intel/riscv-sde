"""
Configuration file for the Sphinx documentation builder.
"""

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('_ext'))

# -- Project information -----------------------------------------------------
project = 'RISC-V Silicon Design Environment'
copyright = '2025, monib-intel'
author = 'monib-intel'
version = '1.0'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx_rtd_theme',
    'myst_parser',
    'mermaid_lexer',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Enable markdown support
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for Auto Section Label --------------------------------------------
autosectionlabel_prefix_document = True
suppress_warnings = ['autosectionlabel.*']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files
html_static_path = ['_static']

# Enable todo notes
todo_include_todos = True

# Cross-references between documents
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Autodoc settings
autodoc_member_order = 'bysource'
autoclass_content = 'both'
