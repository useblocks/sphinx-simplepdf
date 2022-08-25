Quickstart
==========

Install via ``pip install sphinx-simplepdf``.

Then inside your Sphinx documentation folder run ``make simplepdf``. Your PDF is available under ``_build/simplepdf``.

Color and images can be changed by setting ``simplepdf_vars`` inside your ``conf.py`` file:

.. code-block:: python

   simplepdf_vars = {
       'primary': '#333333',
       'links': '#FF3333',
   }

For more configuration options take a look into :ref:`configuration`.

For PDF/HTML specific content, use the ``if-builder`` directive.

.. code-block:: python

   # conf.py
   extensions = ['sphinx_simplepdf']

.. code-block:: rst

   # rst file
   .. if-builder:: simplepdf

      .. toctree::

         my_files
         specific_pdf_file

   .. if-builder:: html

      .. toctree::

         my_files

      Other HTML specific content, which will not be part of the PDF.
