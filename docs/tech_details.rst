Technical details
=================
The sphinx-simplepdf registers the following stuff:

* A sphinx builder, called ``simplepdf``.
* A sphinx theme, called ``sphinx-simplepdf``.

Workflow
--------

1. User calls ``make simplepdf``.
2. ``simplepdf`` builder overwrites theme to use ``sphinx-simplepdf``.
3. Builder generates ``main.css` from ``main.scss`` files.
   Injects also config-vars from ``simplepdf_vars``.
4. Builder starts a `SingleFileHTML` based build.
5. Sphinx creates one single ``index.html``.
6. Builders starts ``weasyprint`` with ``index.html`` as input
7. Done, PDF file exists under ``_build/simplepdf``.
