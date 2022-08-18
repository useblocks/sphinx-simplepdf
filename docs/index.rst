.. sphinx-simplepdf documentation master file, created by
   sphinx-quickstart on Wed Aug 17 12:50:37 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sphinx-SimplePDF
================

This Sphinx extension provides an eas way to build beautiful PDFs based on CSS rules.

It contains:

 * A PDF specific, CSS based Sphinx theme: ``sphinx_simplepdf``.
 * A Sphinx builder, called ``simplepdf``

It is using `weasyprint <https://weasyprint.org/>`__ as PDF generator.

.. image:: /_static/sphinx_simplepdf.png
   :align: center
   :width: 40%
   :target: _static/Sphinx-SimplePDF.pdf

:download:`Download or show Sphinx-SimplePDF </_static/Sphinx-SimplePDF.pdf>`.

.. note::

    This extension is in an early alpha phase.

    It is not bug free and documentation is also missing a lot of stuff.
    You can help us to make it better by reporting bugs or even better by providing code/docs
    changes via a PR.
    The code is stored on github: `useblocks/sphinx-simplepdf <https://github.com/useblocks/sphinx-simplepdf>`__


Quickstart
----------

Install via ``pip install sphinx-simplepdf``.

Then inside your Sphinx documentation folder run ``make simplepdf``. Your PDF is avaialble under ``_build/simplepdf``.

Color and images can be changed by setting ``simplepdf_vars`` inside your ``conf.py`` file:

.. code-block:: python

   simplepdf_vars = {
       'primary': '#333333',
       'links': 'FF3333',
   }


.. toctree::
   :caption: Content
   :maxdepth: 2

   installation
   building
   configuration
   css
   tech_details
   examples/index

One last thing ...
------------------
This theme is heavily based on the excellent work of `Nekmo <https://github.com/Nekmo>`__ for the
`Sphinx Business Theme <https://github.com/Nekmo/sphinx-business-theme>`__.

Without this work, this theme would never exist. Thanks for it ♥





