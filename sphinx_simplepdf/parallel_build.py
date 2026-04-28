"""Optional parallel simplepdf subprocess during non-simplepdf builds."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from sphinx.util import logging

logger = logging.getLogger(__name__)

# Standard HTML-site builders only; simplepdf is omitted so it never nests another simplepdf run.
_PARALLEL_PDF_HTML_BUILDERS = frozenset({"html", "dirhtml", "singlehtml"})


def _parallel_pdf_runs_for_builder(app) -> bool:
    return app.builder.name in _PARALLEL_PDF_HTML_BUILDERS


def _configured_pdf_source(app, output_dir: Path) -> Path:
    """Path to the PDF under the simplepdf build output (matches the simplepdf builder)."""
    raw = app.config.simplepdf_file_name
    if raw:
        return output_dir / Path(str(raw))
    return output_dir / f"{app.config.project}.pdf"


def _configured_pdf_dest(app, html_outdir: Path) -> Path:
    """Destination path under the HTML output directory (flat basename, like a normal artifact)."""
    raw = app.config.simplepdf_file_name
    if raw:
        return html_outdir / Path(str(raw)).name
    return html_outdir / f"{app.config.project}.pdf"


class _PdfGenerator:
    """Manages an optional parallel simplepdf subprocess build."""

    def __init__(self, app):
        self.app = app
        self.process = None
        self.build_dir = None
        self.log_path = None
        self._log_fh = None

    def _on_builder_inited(self, app):
        if not app.config.simplepdf_parallel_build:
            return
        if not _parallel_pdf_runs_for_builder(app):
            return

        self._start_subprocess(app)

    def _on_build_finished(self, app, exception):
        if not app.config.simplepdf_parallel_build:
            return
        if not _parallel_pdf_runs_for_builder(app):
            return

        if exception:
            logger.warning("sphinx-simplepdf: skipping PDF due to build error")
            self._cleanup()
            return

        if self.process is None:
            return

        if self.process.poll() is None:
            logger.info("sphinx-simplepdf: waiting for PDF build to finish...")
        self.process.wait()

        if self.process.returncode != 0:
            log_hint = f"  see log: {self.log_path}" if self.log_path else ""
            logger.warning(f"sphinx-simplepdf: PDF build failed (exit {self.process.returncode}){log_hint}")
            self._cleanup()
            return

        self._copy_pdf(app)
        self._cleanup()

    def _start_subprocess(self, app):
        self.build_dir = Path(tempfile.mkdtemp(prefix="simplepdf_"))
        self.log_path = self.build_dir / "build.log"

        cmd = [
            sys.executable,
            "-m",
            "sphinx",
            "-b",
            "simplepdf",
            str(app.srcdir),
            str(self.build_dir / "output"),
            "-d",
            str(self.build_dir / "doctrees"),
            "-q",
        ]

        logger.info("sphinx-simplepdf: starting PDF build subprocess")
        self._log_fh = self.log_path.open("w")
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=self._log_fh,
            stderr=subprocess.STDOUT,
        )

    def _copy_pdf(self, app):
        if self.build_dir is None:
            return

        output_dir = self.build_dir / "output"
        html_out = Path(app.outdir)
        expected_path = _configured_pdf_source(app, output_dir)
        target = _configured_pdf_dest(app, html_out)

        if expected_path.is_file():
            shutil.copy2(expected_path, target)
            logger.info(f"sphinx-simplepdf: {expected_path.name} -> {target}")
            return

        logger.warning("sphinx-simplepdf: expected PDF not found at %s", expected_path)

    def _stop_pdf_subprocess(self):
        """If the PDF child is still running, stop it before temp dir removal."""
        proc = self.process
        if proc is None:
            return
        if proc.poll() is not None:
            self.process = None
            return
        logger.info("sphinx-simplepdf: terminating PDF build subprocess (primary build failed)")
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            logger.warning("sphinx-simplepdf: PDF subprocess did not exit after terminate; killing")
            proc.kill()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("sphinx-simplepdf: PDF subprocess did not respond to kill")
        self.process = None

    def _cleanup(self):
        self._stop_pdf_subprocess()
        if self._log_fh is not None:
            try:
                self._log_fh.close()
            finally:
                self._log_fh = None
        if self.build_dir is not None:
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir, ignore_errors=True)
            self.build_dir = None


def register(app):
    """Register config and Sphinx event hooks for parallel PDF builds."""
    app.add_config_value("simplepdf_parallel_build", False, "env", types=[bool])

    gen = _PdfGenerator(app)
    app.connect("builder-inited", gen._on_builder_inited)
    # Sphinx invokes listeners in ascending priority order (default 500); 101 runs before most.
    app.connect("build-finished", gen._on_build_finished, priority=101)
