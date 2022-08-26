# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx
import datetime

project = 'Sphinx-SimplePDF'
copyright = '2022, team useblocks'
author = 'team useblocks'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_simplepdf',
    'sphinxcontrib.plantuml',
    'sphinxcontrib.needs',
    'sphinx_copybutton',
]

version = "1.4"

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

plantuml_output_format = "svg_img"

simplepdf_vars = {
    'cover-overlay': 'rgba(150, 26, 26, 0.7)',
    'cover-bg': 'url(cover-bg.jpg) no-repeat center'
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'sphinx_immaterial'
html_theme = 'alabaster'
#html_theme = 'sphinx_needs_pdf'
html_static_path = ['_static']

html_theme_options = {
    'github_user': 'useblocks',
    'github_repo': 'sphinx-simplepdf',
    'fixed_sidebar': True,
    'github_banner': True,
    'github_button': False,
}

html_context = {
    'docs_scope': 'external',
    'cover_logo_title': '',
    'cover_meta_data': 'The simple PDF builder for Sphinx.',
    'cover_footer': f'Build: {datetime.datetime.now().strftime("%d.%m.%Y")}<br>'
                    f'Maintained by <a href="https://useblocks.com">team useblocks</a>',
}


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

