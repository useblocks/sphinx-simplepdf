Changelog
=========

Release 1.6
-----------
:released: 20.01.2023

* **Bugfix** [#60] Fix TOC hrefs for sections that use file title anchors.
* **Enhancement** [#62] Added config option to build PDFs with the weasyprint Python API instead of the binary. 

Release 1.5
-----------
:released: 26.10.2022

* **Enhancement**: ``nocover`` option for :ref:`theme_options`.
* **Enhancement**: New config options to directly configue the weasyprint build.
* **Enhancement**: New config option :ref:`simplepdf_file_name` allows to specify the output file name.
* **Enhancement**: Provides :ref:`pdf-include` directive to embed PDF files in HTML views.

Release 1.4
-----------
:released: 22.09.2022

* **Enhancement**: Adds ``simplepdf_debug`` option, to collect and print some environment specific details.
* **Enhancement**: Adds `demo` PDF to test various layout & style elements.
* **Enhancement**: Replace not-open fonts with open-source fonts.
* **Enhancement**: All fonts are provided by this package. No pre-installed fonts are needed.
* **Enhancement**: [#19] Simple PDF customization with header and bottom page content
* **Enhancement**: Add class wrapper to switch paper orientation, e.g. for large tables
* **Enhancement**: Tables font-size and padding can be reduced by using ``ssp-tinier`` or ``ssp-tiny``.
* **Bugfix**: [#34] handling word wrap in tables
* **Bugfix**: Image handling is done much better.
* **Bugfix**: Font location fixes -> No fonts warnings anymore.
* **Bugfix**: ``html_theme_options`` gets overwritten to suppress Sphinx warnings.
* **Bugfix**: HTML file operations are using hard-coded `utf-8` de/encoding.

Release 1.3
-----------
:released: 25.08.2022

* **Improvement**: file-path in `url()` css configs are now relative to the Sphinx ``_static`` folder.
* **Improvement**: Toctree is working and page numbers are added.
* **Improvement**: Introducing :ref:`if-builder` to control content based on builder.

Release 1.2
-----------
:released: 19.08.2022

* **Improvement**: Overwriting some html_config vars, which are not supported by simplepdf during a PDF build.

Release 1.1
-----------
:released: 19.08.2022

* **Bugfix**: Adds missing scss files to installation package.
* **Bugfix**: Better cover image handling.

Release 1.0
-----------
:released: 18.08.2022
