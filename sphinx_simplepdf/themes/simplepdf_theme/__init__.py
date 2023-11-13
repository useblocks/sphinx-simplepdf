"""Sphinx ReadTheDocs theme.
From https://github.com/ryan-roemer/sphinx-bootstrap-theme.
"""
import logging
from os import path

import sass
from sphinx.application import Sphinx

__version__ = '0.1.0'
__version_full__ = __version__

logger = logging.getLogger(__name__)


def get_html_theme_path() -> str:
    return path.abspath(path.dirname(__file__))


def compile_css(app: Sphinx):
    # Generate main.css
    logger.info("Generating css files from scss-templates")
    css_folder = path.join(app.outdir, f"_static")
    scss_folder = path.join(get_html_theme_path(), "static", "styles", "sources")

    sass.compile(
        dirname=(scss_folder, css_folder),
        output_style="nested",
        custom_functions={
            sass.SassFunction(
                "config",
                ("$a", "$b"),
                app.config.simplepdf_vars.get
            ),
            sass.SassFunction(
                "theme_option",
                ("$a", "$b"),
                app.config.simplepdf_theme_options.get
            ),
        },
    )


# See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
def setup(app: Sphinx):
    app.add_html_theme('simplepdf_theme', get_html_theme_path())
    app.connect('builder-inited', compile_css)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
