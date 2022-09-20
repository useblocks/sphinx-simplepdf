.. _css:

CSS voodoo
==========
The PDF layout is configured via CSS files and their definitions.

You can use some Sphinx mechanism to set specific CSS class inside the rst, so that you can control the output a
little bit.

Predefined css classes
----------------------

Page breaks
~~~~~~~~~~~
Some Sphinx directives allow to use the option ``:class:``.

If this is set to ``break``, then a page break will be introduced in front of the element.

**Example**::

    .. csv-table:: CSV Table
       :file: example.csv
       :class: break

Page Orientation
~~~~~~~~~~~~~~~~

The default orientation is portrait. To change the page orientation for a side, you can add the css class
``ssp-landscape`` to

* directives supporting the option ``:class:``
* or by using the ``.. rst-class::`` directive in the document with classes as arguments
* or by using the ``.. container::`` directive with the options for the used classes

**Example**::

    .. rst-class:: break_before, ssp-landscape, break_after

    .. csv-table:: CSV Table
       :file: example.csv

If the default page orientation is changed to landscape, you can use ``ssp-portrait`` to change to portrait.

Table content wrap
~~~~~~~~~~~~~~~~~~

By default table content is wrapped at whitespaces. If you have table content that can not be wrapped due to
side limitations, the table is drawn out of the margins. This behaviour can be changed by using the css class
``ssp-table-wrap``. This allows the table to break the content anywhere.

This requires a fixed table layout, so you have to set the ``widths`` options (or e.g. ``colwidths`` option
in needtable) to get good results.

This option is by default added to all ``Sphinx-Needs`` elements or could be explicitly set by applying the
``ssp-table-wrap`` as ``style`` option to ``Sphinx-Needs`` directives.

**Example**::

    .. list-table::
        :widths: 10,80
        :class: ssp-table-wrap

Sphinx-Needs elements
~~~~~~~~~~~~~~~~~~~~~

This works also for most Sphinx-Needs elements.

**Example**::

    .. spec:: Specification Example
       :id: SPEC_001
       :style: break

or for ``needtable``::

    .. needtable::
       :filter: 'sphinx' in tags
       :class: break

Customizing theme
-----------------

config() functions
~~~~~~~~~~~~~~~~~~
Inside ``scss`` files you can use ``config(name, default)`` to get access to the values from
``simplepdf_vars``.

The **default** values is used, if the **name** can not be found inside ``simplepdf_vars``, which is the normal case, as
``simplepdf_vars`` is an empty dictionary by default.
