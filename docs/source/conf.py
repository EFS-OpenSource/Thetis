#  ****************************************************************************
#  Configuration file for the Sphinx documentation builder.
#
#  @copyright (c) 2023 e:fs TechHub GmbH. All rights reserved.
#  Dr.-Ludwig-Kraus-Straße 6, 85080 Gaimersheim, DE, https://www.efs-techhub.com
#  ****************************************************************************


import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

from thetis import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'thetis'
copyright = '2023, e:fs TechHub GmbH'
author = 'e:fs TechHub GmbH'

# The full version, including alpha/beta/rc tags
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'myst_parser',
    "sphinxjp.themes.basicstrap",
    "sphinxcontrib.bibtex",
]

bibtex_bibfiles = ['bibliography.bib']

autodoc_default_options = {
    'inherited-members': False,
    'members': True,
}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'basicstrap'

html_title = "Thetis User Guide"
html_short_title = "Thetis User Guide"
html_show_copyright = False
html_show_sphinx = False
html_sidebars = { '**': ['globaltoc.html', 'searchbox.html'] }

html_static_path = ['_static']

html_context = {
    'css_files': ['_static/css/text.css', '_static/css/toggle.css'],
}