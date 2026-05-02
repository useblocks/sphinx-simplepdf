"""Tests for simplepdf_html_hook configuration."""

import pytest
from sphinx.errors import ConfigError, ExtensionError

from .utils import build_and_capture_stdout


def test_html_hook_valid_builds(sphinx_build, capsys):
    """Configured hook script loads and build completes."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="html_hook")
    assert result.pdf_exists()
    assert not result.has_warnings("ERROR:")


def test_html_hook_missing_file_raises(sphinx_build):
    with pytest.raises(ConfigError, match="not found"):
        sphinx_build(
            srcdir="html_hook",
            confoverrides={"simplepdf_html_hook": "./does_not_exist_hook.py"},
        ).build()


def test_html_hook_missing_function_raises(sphinx_build):
    with pytest.raises(ConfigError, match="html_hook"):
        sphinx_build(
            srcdir="html_hook",
            confoverrides={"simplepdf_html_hook": "hooks/missing_def.py"},
        ).build()


def test_html_hook_returns_none_raises(sphinx_build):
    with pytest.raises(ExtensionError, match="returned None"):
        sphinx_build(
            srcdir="html_hook",
            confoverrides={"simplepdf_html_hook": "hooks/returns_none.py"},
        ).build()
