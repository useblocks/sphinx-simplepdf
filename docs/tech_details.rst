Technical details
=================
The sphinx-simplepdf registers the following stuff:

A sphinx builder, called ``simplepdf``. Code inside ``/builders/simplepdf.py``.

A sphinx theme, called ``sphinx-simplepdf``. Files under ``/themes/sphinx_simplepdf``.

During package installation, builder and theme get registered for Sphinx. This is done via the ``enytry__points``
mechanism.

.. literalinclude:: ../setup.py
   :lines: 32-39

Workflow
--------

1. User calls ``make simplepdf``.
2. ``simplepdf`` builder overwrites theme to use ``sphinx-simplepdf``.
3. Builder generates ``main.css`` from ``main.scss`` files.
   Injects also config-vars from ``simplepdf_vars``.
4. Builder starts a **SingleFileHTML** based build.
5. Sphinx creates one single ``index.html``.
6. Builders starts **weasyprint** with ``index.html`` as input
7. Done, PDF file exists under ``_build/simplepdf``.
