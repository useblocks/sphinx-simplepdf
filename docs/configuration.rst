.. _configuration:

Configuration
=============

simplepdf_vars
--------------

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
~~~~~~~~~~~

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
~~~~~~~~
The values from the configuration are taken as they are and injected into ``scss`` files, which are used to generate
the css files. So each value or command, which is supported by ``scss``, can be set.

Color selection
+++++++++++++++
.. code-block:: python

   simplepdf_vars = {
       'primary': '#FA2323',
       'cover-overlay': 'rgba(250, 35, 35, 0.5)',
   }

File references
+++++++++++++++
.. code-block:: python

   simplepdf_vars = {
       'cover-bg': 'url(cover-bg.jpg) no-repeat center'
   }

The file path must be relative to the Sphinx _static folder.
So in the above example the image is stored under ``/_static/cover-bg-jpg``.

SimplePDF docs
++++++++++++++
This is ``simplepdf_vars`` as it is used inside the **Sphinx-SimplePDF** ``conf.py`` file:

.. literalinclude:: conf.py
   :lines: 31-34


simplepdf_debug
----------------
A boolean value. If set to ``True``, **Sphinx-SimplePDF** will add some debug information add the end of the PDF.

This contains data about the used Python Environment and the Sphinx project.
It is mainly used if any problems occur and extra information is needed.

``simplepdf_debug = True``

You can see an example in our :download:`PDF Demo <_static/Sphinx-SimplePDF-DEMO.pdf>` at the end of the file.

.. warning::

   The debug output contains absolute file paths and maybe other critical information.
   Do not use for official PDF releases.

simplepdf_weasyprint_flags
--------------------------
List of flags to pass to **weasyprint** subprocess. This may be helpfull in debugging the pdf creation

``simplepdf_weasyprint_flags = ['-v']``

.. warning::

   The flags should only pass switches to **weasyprint**, input and output file names are appended by **Sphinx-SimplePDF**

simplepdf_weasyprint_timeout
----------------------------

In rare cases **weasyprint** seems to run into infinite loops during processing of the input file.
To avoid blocking CI jobs a timeout can be configured. The build is aborted with a `` subprocess.TimeoutExpired¶`` exception.

``simplepdf_weasyprint_timeout = 300``
