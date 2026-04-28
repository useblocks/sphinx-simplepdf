Building PDF
============

Inside your ``docs`` folder, run::

  make simplepdf

or for more control::

  sphinx-build -M simplepdf . _build

.. note:: To produce a PDF during ``html``, ``dirhtml``, or ``singlehtml`` builds (for example ``make html``), enable
   :ref:`simplepdf_parallel_build` in :doc:`configuration`.
