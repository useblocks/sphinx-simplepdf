"""Theme registers for Sphinx but does not define get_scss_sources_path (fallback case)."""

from pathlib import Path
import sys

_doc = Path(__file__).resolve().parent
if str(_doc) not in sys.path:
    sys.path.insert(0, str(_doc))

project = "MissingScssHookTest"
extensions = ["sphinx_simplepdf", "stub_theme_no_scss_hook"]
master_doc = "index"
exclude_patterns = ["_build"]

simplepdf_theme = "stub_theme_no_scss_hook"
