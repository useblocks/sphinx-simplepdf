Directives
==========

.. _if-builder:

if-builder
----------

``if-builder`` can be used to define builder specific content.

The content of the directive gets added to the documentation only, if the provided directive argument matches the
chosen builder name. The argument is case-insensitive.

**Example**

.. code-block:: rst

   .. if-builder:: simplepdf

      .. toctree::

         my_files
         specific_pdf_file

   .. if-builder:: html

      .. toctree::

         my_files

      Other HTML specific content, which will not be part of the PDF.

.. code-block:: bash

   # Call examples
   make simplepdf
   sphinx-build -M html . _build

.. warning::

   ``if-builder`` may not be taken into account, if a Sphinx incremental build is performed.
   Be sure to always use a clean first build, after a builder switch.

.. note:: Why not using the ``.. only::`` directive?

   The ``only`` directive works differently and does not support for instance ``toctree`` and other mechanism for
   controlling the documentation structure.

