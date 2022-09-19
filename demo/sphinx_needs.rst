
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


.. req:: Sphinx-Needs Theme extension support with code examples
   :id: REQ_002
   :status: done
   :tags: sphinx, extension

   The ``Sphinx-Needs Theme`` for PDF shall support also code examples or inline codes with long text

   This_is_a_non_breakable_line_due_to_no_whitespaces_in_text_at_all_which_is_not_readable_without_breaking_it_working_if_you_can_read_THIS


Sphinx-Needs tables
===================

.. needtable::
   :filter: 'sphinx' in tags
   :columns: id, title, status, tags

This is the same table, but with datatables style. This normally adds a scrollbar to tables if extending the normal layout size

.. needtable::
   :filter: 'sphinx' in tags
   :style: datatables
   :class: table-wrap
   :colwidths: 10,10,10,10,60
   :columns: id, title, status, tags, content


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


