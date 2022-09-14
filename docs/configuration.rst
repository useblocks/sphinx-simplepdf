.. _configuration:

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
       'links': 'FA2323',
       'cover-bg' 'url(cover-bg.jpg) no-repeat center'
       'cover-overlay': 'rgba(250, 35, 35, 0.5)',
       'top-left-content': 'counter(page)',
       'bottom-center-content': '"Custom footer content"',
   }

This values are used then inside the scss files, which define the PDF layout.

Config vars
-----------

:primary: Primary color
:primary_opaque: Primary color with opaqueness. Example ``rgba(150, 26, 26, .5)``
:secondary: Secondary color
:cover: Text color on the cover
:white: A color representing white
:links: Color for links
:cover-bg: Cover background image. Can be a single color or even an image path.
:cover-overlay: RBG based color overlay for the cover-image. Example: ``rgba(250, 35, 35, 0.5)``
:top-left-content: Text or css function to display on pdf output. Example: ``counter(page)``
:top-center-content: Text or css function to display on pdf output.
:top-right-content: Text or css function to display on pdf output.
:bottom-left-content: Text or css function to display on pdf output.
:bottom-center-content: Text or css function to display on pdf output.
:bottom-right-content: Text or css function to display on pdf output.


All variables are defined inside ``/themes/sphinx_simplepdf/sttuc/stles/sources/_variables.scss``.

.. hint::

   If a content-string shall be set, please make sure to use extra `"` around the string.
   Example: `'bottom-center-content': '"Custom footer content"'`.

Examples
--------
The values from the configuration are taken as they are and injected into ``scss`` files, which are used to generate
the css files. So each value or command, which is supported by ``scss``, can be set.

Color selection
~~~~~~~~~~~~~~~
.. code-block:: python

   simplepdf_vars = {
       'primary': '#FA2323',
       'cover-overlay': 'rgba(250, 35, 35, 0.5)',
   }

File references
~~~~~~~~~~~~~~~
.. code-block:: python

   simplepdf_vars = {
       'cover-bg': 'url(cover-bg.jpg) no-repeat center'
   }

The file path must be relative to the Sphinx _static folder.
So in the above example the image is stored under ``/_static/cover-bg-jpg``.

SimplePDF docs
~~~~~~~~~~~~~~
This is ``simplepdf_vars`` as it is used inside the **Sphinx-SimplePDF** ``conf.py`` file:

.. literalinclude:: conf.py
   :lines: 31-34


