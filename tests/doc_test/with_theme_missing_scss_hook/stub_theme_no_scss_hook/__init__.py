"""Sphinx theme without get_scss_sources_path — SimplePDF must fall back to bundled SCSS."""

from os import path


def setup(app):
    app.add_html_theme("stub_theme_no_scss_hook", path.abspath(path.dirname(__file__)))
    return {"parallel_read_safe": True, "parallel_write_safe": True}
