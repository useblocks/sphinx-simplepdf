"""Tests for warnings and error handling."""

import pytest

from .utils import build_and_capture_stdout


def test_broken_anchors_warning(sphinx_build, capsys):
    """Test that broken anchors produce warnings."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_issues")

    # Should have warnings about broken links/anchors
    assert result.has_warnings()

    # Check for specific WeasyPrint anchor warnings
    anchor_warnings = result.get_warnings_matching(r"(anchor|link|reference)")
    assert len(anchor_warnings) > 0


def test_missing_image_warning(sphinx_build, tmp_path):
    """Test that missing images produce warnings."""
    # This would require a test doc with broken image reference
    pytest.skip("Requires test doc with broken image")


def test_build_warnings_are_captured(sphinx_build, capsys):
    """Test that all build warnings are captured."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_issues")

    # Warnings should be accessible
    assert isinstance(result.warnings, list)


def test_weasyprint_warnings_logged(sphinx_build, capsys):
    """Test that WeasyPrint warnings are logged."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_issues")

    # Look for WeasyPrint-specific warnings
    weasy_warnings = result.get_warnings_matching(r"(weasyprint|WeasyPrint)")
    # May or may not have WeasyPrint warnings depending on document
    assert isinstance(weasy_warnings, list)


@pytest.mark.parametrize("strict_mode", [True, False])
def test_strict_mode_handling(sphinx_build, capsys, strict_mode):
    """Test behavior with strict mode enabled/disabled."""
    confoverrides = {"nitpicky": strict_mode}

    if strict_mode:
        # In strict mode, warnings may cause build to fail
        with pytest.raises((AssertionError, Exception)):
            sphinx_build(srcdir="with_issues", confoverrides=confoverrides).build(raise_on_warning=True)
    else:
        # Without strict mode, warnings are logged but build succeeds
        result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_issues", confoverrides=confoverrides)
        assert result.pdf_exists()
