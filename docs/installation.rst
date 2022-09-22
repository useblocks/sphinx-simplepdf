Installation
============

From PyPi
---------

.. code-block:: bash

    pip install sphinx-simplepdf

From source
-----------

.. code-block:: bash

   git clone git@github.com:useblocks/sphinx-simplepdf.git
   cd sphinx-simplepdf
   pip install .

Requirements
------------
**Sphinx-SimplePDF** requires **Sphinx version >= 4.4.4** to properly render the Table of Content with page counts.

macOS installation
~~~~~~~~~~~~~~~~~~
If you are using **macOS** as operating system, the chance is high that the package **pango** gets not automatically
installed when installing **Sphinx-SimplePDF**.

In this case please run also ``brew install pango``.

Windows installation
~~~~~~~~~~~~~~~~~~~~
**Sphinx-SimplePDF** is based on WeasypPrint, which is not so easy to get installed on Windows.

Please follow their instructions about
`how to install WeasyPrint on Windows <https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows>`_.



Using Sphinx-SimplePDF directives
---------------------------------
Sphinx-SimplePDF can be called directly after the installation.

However, if you want to use the included directives, like :ref:`if-builder`, you need to add Sphinx-SimplePDF
to the list of extensions in your ``conf.py`` file::

    extensions = [
        'sphinx_simplepdf',
        # additional extensions
    ]



ReadTheDocs configuration
-------------------------
**Sphinx-SimplePDF** can be also used on `Read The Docs (RTD) <https://readthedocs.io>`_ to generate your PDF.
As it is not supported by RTD by default, you need to create a ``.readthedocs.yaml`` configuration file on the root level
of our project.

You can take the one from **Sphinx-SimplePDF** as a good example:

.. literalinclude:: /../.readthedocs.yaml
