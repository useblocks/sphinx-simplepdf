.. _directives:

Directives
==========

.. warning::

   To use the directives, your ``conf.py`` file must contain Sphinx-SimplePDF in the extension list::

       extensions = [
           'sphinx_simplepdf',
           # additional extensions
       ]



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

.. _if-include:

if-include
----------

``if-include`` can be used to include files only when the specified builder is used. This is the same as using a
include nested in a if-builder statement. You can list multiple files and use different builders.

.. code-block:: rst
   
   .. if-builder:: simplepdf

      .. include:: ./path/to/my/file.xy

      .. include:: ./path/to/my/other/file.xy


is the same as

.. code-block:: rst
   
   .. if-include:: simplepdf 
      
      ./path/to/my/file.xy
      ./path/to/my/other/file.xy

.. warning::
   in some cases content meant for html only builds will get included in the PDF if you build the html documentation
   and do not delete the build files.

   Always make sure to use ``make clean`` or similar to delete build files before building the PDF.


The following chapter should only be visible in the PDF version of this documentation

.. if-include:: simplepdf  

   ./if_pdf_include.rst

.. _pdf-include:

pdf-include
-----------
Includes a PDF file inside the the HTML code.
The browser decides mostly, what kind of PDF-viewer.


.. code-block:: rst

   .. pdf-include:: _static/SimplePDF_test.pdf


.. pdf-include:: _static/SimplePDF_test.pdf


Options
~~~~~~~

.. contents::
   :local:

For more options of how to configure the PDF viewer, take a look into the documentation of
`sphinxcontrib-pdfembed <https://github.com/SuperKogito/sphinxcontrib-pdfembed#parameters>`_

width / height
~~~~~~~~~~~~~~
Provide a number and unit for width/height.

Examples: ``:width: 50%``, ``height: 800px``.

| Defaults:
| ``:width: 100%``
| ``:height: 400px``.

.. code-block:: rst

   .. pdf-include:: _static/SimplePDF_test.pdf
      :width: 40%
      :height: 200px


.. pdf-include:: _static/SimplePDF_test.pdf
   :width: 40%
   :height: 200px

page
~~~~
Specify the page to show when PDF gets loaded.

Default: `None`

If not given the browser decides what page to open (normally page 1) and may also reuse the last seen page number.

.. code-block:: rst

   .. pdf-include:: _static/SimplePDF_test.pdf
      :page: 2


.. pdf-include:: _static/SimplePDF_test.pdf
   :page: 2


toolbar
~~~~~~~
If set to ``0``, the toolbar is hidden in most browsers (seems not to work on Firefox).

Default: ``1``


.. code-block:: rst

   .. pdf-include:: _static/SimplePDF_test.pdf
      :toolbar: 0


.. pdf-include:: _static/SimplePDF_test.pdf
   :toolbar: 0
