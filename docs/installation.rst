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
