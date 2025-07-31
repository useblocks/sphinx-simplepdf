# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sphinx
import datetime
import sys

sys.path.append(os.path.abspath("."))  # Example if `ub_theme` folder is in the same folder as the `conf.py` file

from ub_theme.conf import ub_html_theme_options

project = 'Sphinx-SimplePDF'
copyright = '2022, team useblocks'
author = 'team useblocks'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_simplepdf',
    'sphinxcontrib.plantuml',
    'sphinx_needs',
    'sphinx_immaterial',
    'sphinx_copybutton',
]

version = "1.6.0"

templates_path = ["_templates", "ub_theme/templates"]
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

plantuml_output_format = "svg_img"
local_plantuml_path = os.path.join(os.path.dirname(__file__), "utils", "plantuml.jar")
plantuml = f"java -Djava.awt.headless=true -jar {local_plantuml_path}"

simplepdf_vars = {
    'cover-overlay': 'rgba(150, 26, 26, 0.7)',
    'cover-bg': 'url(cover-bg.jpg) no-repeat center'
}

# use this to force using the weasyprint python API instead of building via the binary
# simplepdf_use_weasyprint_api = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_immaterial'
html_title = 'Sphinx-SimplePDF'
# html_theme = 'alabaster'
# html_theme = 'sphinx_needs_pdf'

html_theme_options = ub_html_theme_options
# You can add other Sphinx-Immaterial theme options like below
other_options = {
    "repo_url": "https://github.com/useblocks/sphinx-simplepdf",
    "repo_name": "sphinx-simplepdf",
    "repo_type": "github",
}
html_theme_options.update(other_options)

html_context = {
    'docs_scope': 'external',
    'cover_meta_data': 'The simple PDF builder for Sphinx.',
}

html_static_path = ["_static", "ub_theme/css", "ub_theme/js"]
html_css_files = ["ub-theme.css"]
html_js_files = ["ub-theme.js"]


def setup_jquery(app, exception):
    """
    Inject jQuery if Sphinx>=6.x

    Staring on Sphinx 6.0, jQuery is not included with it anymore.
    As this extension depends on jQuery, we are including it when Sphinx>=6.x
    """

    if sphinx.version_info >= (5, 0, 0):
        # https://jquery.com/download/#using-jquery-with-a-cdn
        jquery_cdn_url = "https://code.jquery.com/jquery-3.6.0.min.js"
        html_js_files = getattr(app.config, "html_js_files", [])
        html_js_files.append((
            jquery_cdn_url,
            {
                'integrity': 'sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=',
                'crossorigin': 'anonymous'
            }
        ))
        app.config.html_js_files = html_js_files
