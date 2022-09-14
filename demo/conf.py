# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import sphinx
import datetime

sys.path.append(os.path.dirname(__file__))  # Needed for test_py_module

project = 'Sphinx-SimplePDF-DEMO'
copyright = '2022, team useblocks'
author = 'team useblocks'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_simplepdf',
    'sphinxcontrib.plantuml',
    'sphinxcontrib.needs',
    'sphinx_copybutton',
    'sphinx.ext.autodoc',
]

version = "1.0"  # Will not be raised

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

plantuml_output_format = "svg_img"

simplepdf_vars = {
    'cover-overlay': 'rgba(26, 150, 26, 0.7)',
    'cover-bg': 'url(frog.jpg) no-repeat center',
    'primary': '#1a961a',
    'secondary': '#379683',
    'cover': '#ffffff',
    'white': '#ffffff',
    'links': '#1a961a',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_context = {
    'docs_scope': 'external',
    'cover_logo_title': '',
    'cover_meta_data': 'DEMO PDF of Sphinx-SimplePDF',
    'cover_footer': f'Build: {datetime.datetime.now().strftime("%d.%m.%Y")}<br>'
                    f'Maintained by <a href="https://useblocks.com">team useblocks</a>',
}

plantuml_output_format = "svg_img"
local_plantuml_path = os.path.join(os.path.dirname(__file__), "../", "docs", "utils", "plantuml.jar")
plantuml = f"java -Djava.awt.headless=true -jar {local_plantuml_path}"


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

