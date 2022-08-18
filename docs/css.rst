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

Sphinx-Needs objects
~~~~~~~~~~~~~~~~~~~~

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
