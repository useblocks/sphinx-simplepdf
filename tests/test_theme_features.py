"""Tests for SimplePDF theme features."""

import pytest


def test_default_theme_applied(sphinx_build):
    """Test that default SimplePDF theme is applied."""
    result = sphinx_build(srcdir="basic_doc").build()

    assert result.pdf_exists()


def test_custom_theme_settings(sphinx_build):
    """Test that custom theme settings are applied."""
    result = sphinx_build(
        srcdir="basic_doc",
        confoverrides={
            "simplepdf_theme_options": {
                "primary_color": "#FF0000",
            }
        },
    ).build()

    assert result.pdf_exists()


def test_toc_generation(sphinx_build):
    """Test that table of contents is generated."""
    result = sphinx_build(srcdir="with_toc", confoverrides={"simplepdf_toc": True}).build()

    assert result.pdf_exists()


@pytest.mark.parametrize("font_size", ["10pt", "12pt", "14pt"])
def test_different_font_sizes(sphinx_build, font_size):
    """Test PDF generation with different font sizes."""
    result = sphinx_build(srcdir="basic_doc", confoverrides={"simplepdf_font_size": font_size}).build()

    assert result.pdf_exists()
