"""Central pytest configuration and fixtures for sphinx-simplepdf tests."""

from __future__ import annotations

import io
import logging
from pathlib import Path
import re
import shutil
from typing import Any

import pytest
from sphinx.application import Sphinx
from sphinx.testing.util import SphinxTestApp
from sphinx.util import logging as sphinx_logging

from .imgcompare import compare_pdfs

pytest_plugins = ("sphinx.testing.fixtures",)


def copy_srcdir_to_tmpdir(srcdir: Path, tmp: Path) -> Path:
    """
    Copy Source Directory to Temporary Directory.

    This function copies the contents of a source directory to a temporary
    directory. It generates a random subdirectory within the temporary directory
    to avoid conflicts and enable parallel processes to run without conflicts.

    :param srcdir: Path to the source directory.
    :param tmp: Path to the temporary directory.

    :return: Path to the newly created directory in the temporary directory.
    """
    srcdir = Path(__file__).parent.absolute() / srcdir
    tmproot = tmp / Path(srcdir).name
    shutil.copytree(srcdir, tmproot)
    return tmproot


@pytest.fixture(scope="session")
def rootdir():
    """Root directory for test documentation projects."""
    return Path(__file__).parent / "doc_test"


@pytest.fixture(scope="session")
def refdir():
    """Root directory for test documentation projects."""
    return Path(__file__).parent / "ref_pdfs"


@pytest.fixture
def content(request):
    """
    Provide test document content dynamically.

    Usage in test:
        @pytest.mark.parametrize('content', [
            {'index.rst': '.. title::\n\n   Test\n'}
        ], indirect=True)
        def test_example(app):
            ...
    """
    return request.param if hasattr(request, "param") else {}


class SphinxBuild:
    """Helper class to build Sphinx documentation and access results."""

    def __init__(self, app: Sphinx, src: Path, status: io.StringIO, warning: io.StringIO):
        self.app: Sphinx = app
        self.src: Path = src
        self.outdir: Path | None = None
        self.warnings: list[str] = []
        self.errors: list[str] = []
        self.status_stream: io.StringIO = status
        self.warning_stream: io.StringIO = warning
        self.debug_output: list[str] = []
        self.pngs: list[Path] = []

    def build(self, force_all: bool = True, raise_on_warning: bool = False, debug: bool = False):
        """
        Build the documentation.

        Args:
            force_all: Rebuild all files
            raise_on_warning: Raise exception on warnings
        """

        if debug:
            self.app.verbosity = 2

            debug_buffer = io.StringIO() if debug else None

            # Eigenen Handler OHNE Sphinx-Filter für Debug
            debug_handler = logging.StreamHandler(debug_buffer)
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

            # An Extension-Logger hängen (umgeht Sphinx-Filter!)
            ext_logger = sphinx_logging.getLogger("sphinx_simplepdf")
            ext_logger.logger.addHandler(debug_handler)
            ext_logger.logger.setLevel(logging.DEBUG)
            ext_logger.logger.propagate = False  # Verhindere Doppel-Logging

        self.app.build(force_all=force_all)
        self.outdir = Path(self.app.builder.outdir)

        self.status_output = self.status_stream.getvalue()
        self.warnings = self.warning_stream.getvalue().splitlines()

        if debug:
            self.debug_output = debug_buffer.getvalue().splitlines()

        if raise_on_warning and self.warnings:
            raise AssertionError("Build produced warnings:\n" + "\n".join(self.warnings))

        return self

    def html_content(self, docname: str = "index") -> str:
        """
        Get generated HTML content (before SimplePDF processing).

        Args:
            docname: Document name without extension

        Returns:
            HTML content as string
        """
        if self.outdir is None:
            raise RuntimeError("Build not run yet; outdir is not set")

        html_file = self.outdir / f"{docname}.html"
        if not html_file.exists():
            raise FileNotFoundError(f"HTML file not found: {html_file}")
        return html_file.read_text(encoding="utf-8")

    def processed_html(self) -> str:
        """
        Get processed HTML from SimplePDF builder (from debug output).

        The SimplePDF builder logs the processed HTML before PDF generation.
        This extracts it from the warning stream.

        Returns:
            Processed HTML content as string
        """
        # Look for debug HTML output in warnings
        # (SimplePDF should log processed HTML with specific marker)

        def strip_log_prefix(text):
            """Entferne Log-Level-Prefixe wie 'DEBUG: ', 'INFO: ' etc."""
            return re.sub(r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL):\s*", "", text, flags=re.MULTILINE)

        # print(f"-- debug output--\n{self.debug_output}\n-----")
        for i, line in enumerate(self.debug_output):
            if "DEBUG HTML START" in line:
                # Find end marker
                html_lines = []
                for next_line in self.debug_output[i + 1 :]:
                    if "DEBUG HTML END" in next_line:
                        break
                    html_lines.append(strip_log_prefix(next_line))
                return "\n".join(html_lines)

        raise ValueError("No processed HTML found in debug output")

    def pdf_path(self, basename: str | None = None) -> Path:
        """
        Get path to generated PDF file.

        Args:
            basename: PDF filename without extension (default: project name)

        Returns:
            Path to PDF file
        """
        if basename is None:
            basename = self.app.config.project

        if self.outdir is None:
            raise RuntimeError("Build not run yet; outdir is not set")

        pdf_file = self.outdir / f"{basename}.pdf"
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_file}")
        return pdf_file

    def pdf_exists(self, basename: str | None = None) -> bool:
        """Check if PDF was generated."""
        try:
            self.pdf_path(basename)
            return True
        except FileNotFoundError:
            return False

    def compare_pdf(
        self,
        ref_pdf: Path,
        pages: slice | None = None,
        changed_ratio_threshold: float = 0.001,
        ssim_threshold: float = 0.99,
    ) -> bool:
        if self.outdir is not None:
            return compare_pdfs(
                ref_pdf=ref_pdf,
                pages=pages,
                test_pdf=self.pdf_path(),
                work_dir=Path(self.outdir.parent / "png"),
                changed_ratio_threshold=changed_ratio_threshold,
                ssim_threshold=ssim_threshold,
            )
        else:
            return False

    def has_warnings(self, pattern: str | None = None) -> bool:
        """
        Check if build produced warnings.

        Args:
            pattern: Optional regex pattern to match specific warnings

        Returns:
            True if warnings exist (and match pattern if provided)
        """
        if pattern is None:
            return len(self.warnings) > 0

        import re

        regex = re.compile(pattern)
        return any(regex.search(w) for w in self.warnings)

    def get_warnings_matching(self, pattern: str) -> list[str]:
        """
        Get all warnings matching a pattern.

        Args:
            pattern: Regex pattern to match

        Returns:
            List of matching warning messages
        """
        import re

        regex = re.compile(pattern)
        return [w for w in self.warnings if regex.search(w)]


@pytest.fixture
def sphinx_build(make_app, tmp_path):
    """
    Main fixture to build Sphinx projects with SimplePDF.

    Usage:
        def test_example(sphinx_build):
            app = sphinx_build(
                buildername='simplepdf',
                srcdir='basic_doc',
                confoverrides={'project': 'Test'}
            )
            result = app.build()
            assert result.pdf_exists()
    """

    def _make_build(
        buildername: str = "simplepdf", srcdir: str | None = None, confoverrides: dict[str, Any] | None = None, **kwargs
    ) -> SphinxBuild:
        """
        Create and return SphinxBuild instance.

        Args:
            buildername: Sphinx builder name
            srcdir: Source directory name (relative to doc_test/)
            confoverrides: Dictionary of conf.py overrides
            **kwargs: Additional arguments for make_app

        Returns:
            SphinxBuild instance
        """
        if srcdir is None:
            raise ValueError("srcdir is required")

        # Resolve source directory using pathlib
        test_root = Path(__file__).parent / "doc_test"
        src_path = test_root / srcdir
        src_dir = copy_srcdir_to_tmpdir(Path("doc_test") / srcdir, tmp_path)

        if not src_path.exists():
            raise ValueError(f"Test document directory not found: {src_path}")

        status = io.StringIO()
        warning = io.StringIO()

        # Create app with Path object (Sphinx 8.2 compatible)
        app = make_app(
            buildername=buildername,
            # srcdir=src_path,
            srcdir=src_dir,
            status=status,
            warning=warning,
            confoverrides=confoverrides or {},
            freshenv=True,
            **kwargs,
        )
        return SphinxBuild(app, src_path, status, warning)

    return _make_build


@pytest.fixture
def sphinx_build_factory(tmp_path, rootdir):
    """
    Factory fixture to create multiple test builds.

    More flexible than sphinx_build for tests that need multiple builds.
    """

    def _factory(srcdir: str, buildername: str = "simplepdf", **kwargs):
        src = rootdir / srcdir
        app = SphinxTestApp(buildername=buildername, srcdir=src, freshenv=True, **kwargs)
        status = io.StringIO()
        warning = io.StringIO()
        return SphinxBuild(app, src, status, warning)

    return _factory


@pytest.fixture
def minimal_conf():
    """Minimal conf.py configuration for SimplePDF."""
    return {
        "extensions": ["sphinx_simplepdf"],
        "simplepdf_theme": "simplepdf_theme",
        "master_doc": "index",
        "exclude_patterns": ["_build"],
    }
