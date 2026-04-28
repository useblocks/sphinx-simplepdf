"""Tests for parallel PDF build functionality."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sphinx_simplepdf.parallel_build import _PdfGenerator


class TestPdfGeneratorSkips:
    """Test that the parallel hooks are no-ops when they should be."""

    def _make_app(self, builder_name="html", parallel=True):
        app = MagicMock()
        app.builder.name = builder_name
        app.config.simplepdf_parallel_build = parallel
        app.srcdir = "/tmp/src"
        app.outdir = "/tmp/out"
        return app

    def test_builder_inited_skips_simplepdf_builder(self):
        """No subprocess when the current builder IS simplepdf (not an HTML site builder)."""
        app = self._make_app(builder_name="simplepdf", parallel=True)
        gen = _PdfGenerator(app)
        gen._on_builder_inited(app)
        assert gen.process is None

    def test_builder_inited_skips_non_html_builder(self):
        """No subprocess for builders outside html / dirhtml / singlehtml."""
        app = self._make_app(builder_name="latex", parallel=True)
        gen = _PdfGenerator(app)
        gen._on_builder_inited(app)
        assert gen.process is None

    @pytest.mark.parametrize("builder_name", ["html", "dirhtml", "singlehtml"])
    def test_builder_inited_starts_subprocess_for_html_family(self, builder_name, tmp_path):
        app = self._make_app(builder_name=builder_name, parallel=True)
        app.srcdir = str(tmp_path / "src")
        Path(app.srcdir).mkdir()
        gen = _PdfGenerator(app)
        with patch("sphinx_simplepdf.parallel_build.subprocess.Popen") as mock_popen:
            mock_popen.return_value = MagicMock()
            gen._on_builder_inited(app)
        mock_popen.assert_called_once()
        gen._cleanup()

    def test_builder_inited_skips_when_disabled(self):
        """No subprocess when simplepdf_parallel_build is False."""
        app = self._make_app(parallel=False)
        gen = _PdfGenerator(app)
        gen._on_builder_inited(app)
        assert gen.process is None

    def test_build_finished_skips_simplepdf_builder(self):
        """build-finished is a no-op when builder is simplepdf."""
        app = self._make_app(builder_name="simplepdf", parallel=True)
        gen = _PdfGenerator(app)
        # Should not raise or do anything
        gen._on_build_finished(app, None)
        assert gen.build_dir is None

    def test_build_finished_skips_non_html_builder(self):
        """build-finished ignores parallel PDF when the primary builder is not HTML-site."""
        app = self._make_app(builder_name="latex", parallel=True)
        gen = _PdfGenerator(app)
        proc = MagicMock()
        gen.process = proc
        gen._on_build_finished(app, None)
        proc.wait.assert_not_called()

    def test_build_finished_skips_when_disabled(self):
        """build-finished is a no-op when parallel is disabled."""
        app = self._make_app(parallel=False)
        gen = _PdfGenerator(app)
        gen._on_build_finished(app, None)
        assert gen.build_dir is None

    def test_build_finished_cleans_up_on_exception(self, tmp_path):
        """Temp directory is cleaned up when the primary build fails."""
        app = self._make_app(parallel=True)
        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_test"
        gen.build_dir.mkdir()
        assert gen.build_dir.exists()

        gen._on_build_finished(app, RuntimeError("build error"))
        assert gen.build_dir is None

    def test_build_finished_terminates_running_subprocess_on_exception(self, tmp_path):
        """If the primary build fails, a running PDF subprocess is stopped before cleanup."""
        app = self._make_app(parallel=True)
        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_test"
        gen.build_dir.mkdir()

        proc = MagicMock()
        proc.poll.return_value = None
        proc.wait.return_value = None
        gen.process = proc

        gen._on_build_finished(app, RuntimeError("build error"))

        proc.terminate.assert_called_once()
        proc.wait.assert_called_once_with(timeout=10)
        assert gen.process is None
        assert gen.build_dir is None

    def test_build_finished_noop_when_no_process(self):
        """build-finished does nothing if no subprocess was started."""
        app = self._make_app(parallel=True)
        gen = _PdfGenerator(app)
        gen.process = None
        # Should not raise
        gen._on_build_finished(app, None)


class TestPdfCopy:
    """Test that _copy_pdf copies only PDFs to the output directory."""

    def test_copies_pdf_files(self, tmp_path):
        app = MagicMock()
        app.outdir = str(tmp_path / "html_output")
        Path(app.outdir).mkdir()
        app.config.simplepdf_file_name = None
        app.config.project = "MyProject"

        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_build"
        output = gen.build_dir / "output"
        output.mkdir(parents=True)

        # Create a PDF and some HTML artifacts
        (output / "MyProject.pdf").write_bytes(b"%PDF-fake")
        (output / "index.html").write_text("<html></html>")
        (output / "_static").mkdir()
        (output / "_static" / "style.css").write_text("body {}")

        gen._copy_pdf(app)

        dest = Path(app.outdir)
        assert (dest / "MyProject.pdf").exists()
        assert (dest / "MyProject.pdf").read_bytes() == b"%PDF-fake"
        # HTML artifacts should NOT be copied
        assert not (dest / "index.html").exists()
        assert not (dest / "_static").exists()

    def test_no_pdf_logs_warning(self, tmp_path):
        app = MagicMock()
        app.outdir = str(tmp_path / "html_output")
        Path(app.outdir).mkdir()
        app.config.simplepdf_file_name = None
        app.config.project = "Proj"

        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_build"
        output = gen.build_dir / "output"
        output.mkdir(parents=True)
        # No PDF file created

        with patch("sphinx_simplepdf.parallel_build.logger") as mock_logger:
            gen._copy_pdf(app)
            mock_logger.warning.assert_called_once()
            assert "expected PDF not found" in mock_logger.warning.call_args[0][0]

    def test_noop_when_no_build_dir(self):
        app = MagicMock()
        gen = _PdfGenerator(app)
        gen.build_dir = None
        # Should not raise
        gen._copy_pdf(app)

    def test_copies_to_simplepdf_file_name(self, tmp_path):
        """Reads PDF from the same path the simplepdf builder uses; flattens into HTML outdir."""
        app = MagicMock()
        app.outdir = str(tmp_path / "html_output")
        Path(app.outdir).mkdir()
        app.config.simplepdf_file_name = "docs/handbook.pdf"
        app.config.project = "Ignored"

        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_build"
        output = gen.build_dir / "output"
        nested = output / "docs"
        nested.mkdir(parents=True)
        (nested / "handbook.pdf").write_bytes(b"%PDF-fake")

        gen._copy_pdf(app)

        dest = Path(app.outdir)
        assert (dest / "handbook.pdf").exists()
        assert not (dest / "Ignored.pdf").exists()

    def test_wrong_pdf_name_logs_warning(self, tmp_path):
        """Only the configured output path is used; other PDFs are ignored."""
        app = MagicMock()
        app.outdir = str(tmp_path / "html_output")
        Path(app.outdir).mkdir()
        app.config.simplepdf_file_name = None
        app.config.project = "ReleaseNotes"

        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_build"
        output = gen.build_dir / "output"
        output.mkdir(parents=True)
        (output / "unexpected.pdf").write_bytes(b"%PDF-x")

        with patch("sphinx_simplepdf.parallel_build.logger") as mock_logger:
            gen._copy_pdf(app)

        mock_logger.warning.assert_called_once()
        assert "expected PDF not found" in mock_logger.warning.call_args[0][0]
        assert not (Path(app.outdir) / "ReleaseNotes.pdf").exists()
        assert not (Path(app.outdir) / "unexpected.pdf").exists()


class TestCleanup:
    """Test that _cleanup removes the temp directory."""

    def test_removes_temp_dir(self, tmp_path):
        app = MagicMock()
        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_cleanup"
        gen.build_dir.mkdir()
        (gen.build_dir / "somefile").write_text("data")

        gen._cleanup()
        assert gen.build_dir is None
        assert not (tmp_path / "simplepdf_cleanup").exists()

    def test_clears_build_dir_when_path_already_removed(self, tmp_path):
        """Stale build_dir pointing at a deleted directory should still be cleared."""
        app = MagicMock()
        gen = _PdfGenerator(app)
        gone = tmp_path / "already_removed"
        gen.build_dir = gone
        assert not gone.exists()

        gen._cleanup()
        assert gen.build_dir is None

    def test_noop_when_no_build_dir(self):
        app = MagicMock()
        gen = _PdfGenerator(app)
        gen.build_dir = None
        gen._cleanup()  # should not raise


class TestStartSubprocess:
    """Test that _start_subprocess builds the correct command."""

    def test_command_structure(self, tmp_path):
        app = MagicMock()
        app.srcdir = str(tmp_path / "src")
        Path(app.srcdir).mkdir()

        gen = _PdfGenerator(app)

        with patch("sphinx_simplepdf.parallel_build.subprocess.Popen") as mock_popen:
            mock_popen.return_value = MagicMock()
            gen._start_subprocess(app)

        assert gen.build_dir is not None
        assert gen.log_path is not None

        cmd = mock_popen.call_args[0][0]
        assert cmd[0].endswith("python") or "python" in cmd[0]
        assert cmd[1:4] == ["-m", "sphinx", "-b"]
        assert cmd[4] == "simplepdf"
        assert cmd[5] == str(tmp_path / "src")
        assert "-d" in cmd
        assert "-q" in cmd

        # Cleanup
        gen._cleanup()


class TestBuildFinishedIntegration:
    """Test the full build-finished flow with a mock subprocess."""

    def test_successful_subprocess_copies_pdf(self, tmp_path):
        app = MagicMock()
        app.builder.name = "html"
        app.config.simplepdf_parallel_build = True
        app.config.simplepdf_file_name = None
        app.config.project = "Test"
        app.outdir = str(tmp_path / "html_output")
        Path(app.outdir).mkdir()

        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_build"
        output = gen.build_dir / "output"
        output.mkdir(parents=True)
        (output / "Test.pdf").write_bytes(b"%PDF-test")

        # Mock a completed subprocess
        gen.process = MagicMock()
        gen.process.poll.return_value = 0  # already finished
        gen.process.returncode = 0

        gen._on_build_finished(app, None)

        assert (Path(app.outdir) / "Test.pdf").exists()
        # Temp dir should be cleaned up
        assert gen.build_dir is None

    def test_failed_subprocess_cleans_up(self, tmp_path):
        app = MagicMock()
        app.builder.name = "html"
        app.config.simplepdf_parallel_build = True
        app.config.simplepdf_file_name = None
        app.config.project = "Test"
        app.outdir = str(tmp_path / "html_output")
        Path(app.outdir).mkdir()

        gen = _PdfGenerator(app)
        gen.build_dir = tmp_path / "simplepdf_build"
        gen.build_dir.mkdir()
        gen.log_path = gen.build_dir / "build.log"

        gen.process = MagicMock()
        gen.process.poll.return_value = 1
        gen.process.returncode = 1

        gen._on_build_finished(app, None)

        assert not (Path(app.outdir) / "Test.pdf").exists()
        assert gen.build_dir is None


class TestParallelBuildEndToEnd:
    """End-to-end test using actual Sphinx build with parallel PDF."""

    def test_parallel_build_produces_pdf_in_html_output(self, sphinx_build, capsys):
        """Build as HTML with simplepdf_parallel_build=True and verify PDF appears."""
        result = sphinx_build(
            buildername="html",
            srcdir="basic_doc",
            confoverrides={"simplepdf_parallel_build": True},
        ).build()

        captured = capsys.readouterr()
        result.warnings += captured.out.splitlines()

        # PDF should exist in the HTML output directory
        pdf_files = list(result.outdir.glob("*.pdf"))
        assert len(pdf_files) == 1, f"Expected 1 PDF, found: {pdf_files}"
        assert pdf_files[0].stat().st_size > 0

        # HTML files should also exist (it's an HTML build)
        assert (result.outdir / "index.html").exists()

    def test_parallel_disabled_no_pdf(self, sphinx_build):
        """With parallel disabled, HTML build should not produce a PDF."""
        result = sphinx_build(
            buildername="html",
            srcdir="basic_doc",
            confoverrides={"simplepdf_parallel_build": False},
        ).build()

        pdf_files = list(result.outdir.glob("*.pdf"))
        assert len(pdf_files) == 0
