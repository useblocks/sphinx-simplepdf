"""Basic build tests for SimplePDF."""

import pytest

from .utils import build_and_capture_stdout


def test_basic_build_succeeds(sphinx_build, capsys):
    """Test that a basic document builds successfully."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="basic_doc")

    assert result.pdf_exists()
    assert not result.has_warnings("ERROR:")


def test_html_generation(sphinx_build, capsys):
    """Test that HTML is generated before PDF conversion."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="basic_doc")

    html = result.html_content("index")
    assert "<html" in html
    assert "</html>" in html


def test_build_with_custom_project_name(sphinx_build, capsys):
    """Test that custom project name is used for PDF filename."""
    project_name = "MyCustomProject"
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="basic_doc", confoverrides={"project": project_name})

    assert result.pdf_exists(project_name)
    assert not result.has_warnings("ERROR:")


def test_rebuild_does_not_fail(sphinx_build):
    """Test that rebuilding does not cause errors."""
    builder = sphinx_build(srcdir="basic_doc")

    # First build
    result1 = builder.build()
    assert result1.pdf_exists()

    # Second build
    result2 = builder.build()
    assert result2.pdf_exists()


@pytest.mark.parametrize(
    "srcdir",
    [
        "basic_doc",
        "with_images",
        "with_toc",
    ],
)
def test_various_document_types(sphinx_build, capsys, srcdir):
    """Test that various document types build successfully."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir=srcdir)
    assert result.pdf_exists()
