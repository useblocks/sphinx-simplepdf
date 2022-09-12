
Sphinx-Needs objects
====================

.. req:: Sphinx-Needs Theme extension support
   :id: REQ_001
   :status: done
   :tags: sphinx, extension

   The ``Sphinx-Needs Theme`` for PDF shall support all possible Sphinx extensions an their outcome.


.. spec:: Specification Example
   :id: SPEC_001
   :status: open
   :tags: sphinx, example
   :links: REQ_001
   :layout: complete
   :style: green_border, break

   A specification example with an image.

   .. image:: /_static/example.jpg
      :align: center



Sphinx-Needs tables
===================

.. needtable::
   :filter: 'sphinx' in tags
   :columns: id, title, status, tags

Sphinx-Needs needflow
=====================

Using ``plantuml`` to render image.

.. needflow::
   :filter: 'sphinx' in tags


CSV Table
---------
The following table is too big for the PDF.
There is no way to get a nice looking picture of it.

.. csv-table:: CSV Table
   :file: /_static/example.csv
   :header-rows: 2
   :class: break


