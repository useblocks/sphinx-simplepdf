"""Configuration with table of contents."""

project = "TOCTest"
extensions = ["sphinx_simplepdf"]
master_doc = "index"
exclude_patterns = ["_build"]

simplepdf_theme = "simplepdf_theme"
simplepdf_toc = True
html_css_files = ["custom.css"]
html_static_path = ["_static"]
html_show_sphinx = False
