"""Sphinx project that loads a test-only external PDF theme package."""

from pathlib import Path
import sys

_doc = Path(__file__).resolve().parent
if str(_doc) not in sys.path:
    sys.path.insert(0, str(_doc))

project = "ExternalThemeTest"
extensions = ["sphinx_simplepdf", "stub_external_pdf_theme"]
master_doc = "index"
exclude_patterns = ["_build"]

simplepdf_theme = "stub_external_pdf_theme"
