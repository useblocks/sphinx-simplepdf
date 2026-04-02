"""Tests for PDF generation with WeasyPrint."""

import pytest

from .utils import build_and_capture_stdout, extract_pdf_text, page_count


def test_pdf_is_created(sphinx_build, capsys):
    """Test that PDF file is created."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="basic_doc")

    pdf_path = result.pdf_path()
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0


def test_pdf_contains_content(sphinx_build, capsys):
    """Test that PDF contains actual content (not empty)."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="basic_doc")

    pdf_path = result.pdf_path()
    # PDF should be reasonably sized (> 1KB)
    assert pdf_path.stat().st_size > 1024


def test_pdf_with_images(sphinx_build, capsys):
    """Test that PDF with images is generated."""
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_images")

    # Should build without errors
    assert result.pdf_exists()
    # PDF with images should be larger
    pdf_path = result.pdf_path()
    assert pdf_path.stat().st_size > 5000


def test_pdf_with_toc(sphinx_build, capsys, refdir):
    """Test that PDF with table of contents is generated."""
    # result = sphinx_build(srcdir="with_toc").build()
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_toc", build_kwargs={"debug": True})

    assert result.pdf_exists()
    pdf_path = result.pdf_path()

    # Check for specific WeasyPrint anchor warnings
    anchor_warnings = result.get_warnings_matching(r"(anchor|link|reference)")
    assert len(anchor_warnings) == 0

    assert page_count(pdf_path) == 5

    text = extract_pdf_text(pdf_path)

    assert (
        """
Table of Contents

Contents:

Chapter 1: Getting Started

• Section 1.1
• Section 1.2

Chapter 2: Advanced Topics

• Section 2.1
• Section 2.2

3

3

3

3

3

4
"""
        in text
    )

    assert result.compare_pdf(refdir / "with_toc" / "TOCTest.pdf")


def test_pdf_with_toc_and_typo(sphinx_build, capsys, refdir):
    """Test that PDF with table of contents is generated. PDF has typo, image comparison should fail"""
    # result = sphinx_build(srcdir="with_toc").build()
    result = build_and_capture_stdout(sphinx_build, capsys, srcdir="with_toc_and_typo", build_kwargs={"debug": True})

    assert result.pdf_exists()
    pdf_path = result.pdf_path()

    # Check for specific WeasyPrint anchor warnings
    anchor_warnings = result.get_warnings_matching(r"(anchor|link|reference)")
    assert len(anchor_warnings) == 0

    assert page_count(pdf_path) == 5

    text = extract_pdf_text(pdf_path)

    assert (
        """
Table of Contents

Contents:

Chapter 1: Getting Started

• Section 1.1
• Section 1.2

Chapter 2: Advanced Topcs

• Section 2.1
• Section 2.2

3

3

3

3

3

4
"""
        in text
    )

    assert not result.compare_pdf(refdir / "with_toc" / "TOCTest.pdf", changed_ratio_threshold=0.0001)


@pytest.mark.parametrize("page_format", ["A4", "Letter", "A5"])
def test_pdf_different_page_formats(sphinx_build, capsys, page_format):
    """Test PDF generation with different page formats."""
    result = build_and_capture_stdout(
        sphinx_build, capsys, srcdir="basic_doc", confoverrides={"simplepdf_page_size": page_format}
    )

    assert result.pdf_exists()
