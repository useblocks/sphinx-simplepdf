"""Sphinx ReadTheDocs theme.
From https://github.com/ryan-roemer/sphinx-bootstrap-theme.
"""
from os import path

import sass


__version__ = '0.1.0'
__version_full__ = __version__


def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
    return cur_dir


def create_custom_css(app):

    try:
        simplepdf_vars = app.config.simplepdf_vars
    except AttributeError:
        simplepdf_vars = {}

    def get_config_var(name, default):
        """
        Gets a config variables for scss out of the Sphinx configuration.
        If name is not found in config, the specified default var is returned.

        Args:
            name: Name of the config var to use
            default: Default value, if name can not be found in config

        Returns: Value
        """
        return simplepdf_vars.get(name, default)

    def get_theme_var(name, default):
        """
        Gets a option  variables for scss out of the Sphinx theme options.
        If name is not found in theme options, the specified default var is returned.

        Args:
            name: Name of the option var to use
            default: Default value, if name can not be found in config

        Returns: Value
        """
        return app.config.html_theme_options.get(name, default)

    here = path.abspath(path.dirname(__file__))
    scss_folder = path.join(here, "static", "styles", "sources")

    staticdir = path.join(app.builder.outdir, "_static")

    sass.compile(
        dirname=(scss_folder, staticdir),
        output_style="nested",
        custom_functions={
            sass.SassFunction("config", ("$a", "$b"), get_config_var),
            sass.SassFunction("theme_option", ("$a", "$b"), get_theme_var),
        },
    )


# See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
def setup(app):
    app.add_html_theme('simplepdf_theme', path.abspath(path.dirname(__file__)))
    app.connect('builder-inited', create_custom_css)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
