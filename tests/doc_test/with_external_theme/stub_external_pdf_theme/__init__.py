"""Minimal external theme for tests (Sphinx HTML theme + SimplePDF SCSS hook)."""

from os import path


def get_scss_sources_path():
    """Return SCSS sources for SimplePDF (same layout convention as simplepdf_theme)."""
    return path.join(path.abspath(path.dirname(__file__)), "static", "styles", "sources")


def setup(app):
    app.add_html_theme("stub_external_pdf_theme", path.abspath(path.dirname(__file__)))
    return {"parallel_read_safe": True, "parallel_write_safe": True}
