Configuration
=============

**Sphinx-SimplePDF** provides the config variable ``simplepdf_vars``, which must be a dictionary.
The key is used as identifier inside scss-files and the value must be a css/scss compatible string.

**Example conf.py**

.. code-block:: python

   simplepdf_vars = {
       'primary': '#FA2323',
       'secondary': '#379683',
       'cover': '#ffffff',
       'white': '#ffffff',
       'links': '$primary',
       'cover-overlay': 'rgba(250, 35, 35, 0.5)',
   }

This values are used then inside the scss files, which define the PDF layout.

**Example _cover.scss**

.. code-block:: scss

   background: config("cover-overlay", "rgba(250, 35, 35, 0.6)");

Config vars
-----------

:primary: Primary color
:secondary: Secondary color
:cover: Text color on the cover
:white: A color representing white
:links: Color for links
:cover-bg: Image path to a cover image- Path must be relative to the theme style or an absolute path.
:cover-overlay: RBG based color overlay for the cover-image. Example: ``rgba(250, 35, 35, 0.5)``





