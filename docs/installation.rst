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


ReadTheDocs configuration
-------------------------
**Sphinx-SimplePDF** can be also used on `Read The Docs (RTD) <https://readthedocs.io>`_ to generate your PDF.
As it is not supported by RTD by default, you need to create a ``.readthedocs.yaml`` configuration file on the root level
of our project.

You can take the one from **Sphinx-SimplePDF** as a good example:

.. literalinclude:: /../.readthedocs.yaml
