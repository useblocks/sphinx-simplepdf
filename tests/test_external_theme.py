"""Integration tests for external SimplePDF themes (get_scss_sources_path).

Covers the scenario discussed in PR #134 review: a real importable theme package
whose SCSS is compiled by the simplepdf builder.
"""

from __future__ import annotations

from .utils import build_and_capture_stdout


def test_external_theme_scss_is_compiled(sphinx_build, capsys):
    """An external theme with get_scss_sources_path compiles its own main.scss."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_external_theme")

    assert result.pdf_exists()
    assert not result.has_warnings("ERROR:")
    assert result.outdir is not None
    compiled = (result.outdir / "_static" / "main.css").read_text(encoding="utf-8")
    assert "sphinx-simplepdf-test-external-theme-marker" in compiled
    assert "#2a4b8d" in compiled or "2a4b8d" in compiled


def test_theme_without_get_scss_sources_path_falls_back(sphinx_build, capsys):
    """If the theme module loads but omits get_scss_sources_path, bundled SCSS is used."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_theme_missing_scss_hook")

    assert result.pdf_exists()
    assert not result.has_warnings("ERROR:")
    matched = result.get_warnings_matching(r"does not define get_scss_sources_path")
    assert len(matched) >= 1
