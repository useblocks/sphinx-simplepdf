.. sphinx-simplepdf documentation master file, created by
   sphinx-quickstart on Wed Aug 17 12:50:37 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sphinx-SimplePDF
================

.. toctree::

   installation
   building
   configuration
   css
   tech_details
   examples/index
   changelog


This Sphinx extension provides an easy way to build beautiful PDFs based on CSS rules.



It contains:

 * A PDF specific, CSS based Sphinx theme: ``sphinx_simplepdf``.
 * A Sphinx builder, called ``simplepdf``

It is using `weasyprint <https://weasyprint.org/>`__ as PDF generator.

.. figure:: /_static/sphinx_simplepdf.png
   :align: center
   :width: 40%
   :target: _static/Sphinx-SimplePDF.pdf

   Click image to see PDF  version of this documentation.

.. note::

    This extension is in an early alpha phase.

    It is not bug free and documentation is also missing a lot of stuff.
    You can help us to make it better by reporting bugs or even better by providing code/docs
    changes via a PR.
    The code is stored on github: `useblocks/sphinx-simplepdf <https://github.com/useblocks/sphinx-simplepdf>`__

Quickstart
----------

Install via ``pip install sphinx-simplepdf``.

Then inside your Sphinx documentation folder run ``make simplepdf``. Your PDF is available under ``_build/simplepdf``.

Color and images can be changed by setting ``simplepdf_vars`` inside your ``conf.py`` file:

.. code-block:: python

   simplepdf_vars = {
       'primary': '#333333',
       'links': '#FF3333',
   }

For more configuration options take a look into :ref:`configuration`.

Why another PDF builder?
------------------------
You can use the Sphinx Latex builder to generate PDFs.
And there is also the great `rinohtype <http://www.mos6581.org/rinohtype/master/#>`__ library.

But both have some drawbacks, which we try to avoid with this solution.

Latex distributions are quite big and Latex as language may not be the language of choice for everybody.

rinohtype makes a lot of things easier, but it does not support additional Sphinx extensions very well
(if they are using visitor-functions). For instance is it hard to get PlantUML running with rinohtype.

But for sure, there are also scenarios where **Sphinx-SimplePDF** may not be the best solution.
So if you are unhappy with **Sphinx-SimplePDF** please try the others as well :)

One last thing ...
------------------
This theme is heavily based on the excellent work of `Nekmo <https://github.com/Nekmo>`__ for the
`Sphinx Business Theme <https://github.com/Nekmo/sphinx-business-theme>`__.

Without this work, this theme would never exist. Thanks for it ♥


License
-------

.. literalinclude:: ../LICENSE
