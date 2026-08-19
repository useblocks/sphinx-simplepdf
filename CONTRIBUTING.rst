Contributing to Sphinx-SimplePDF
================================

Thank you for your interest in contributing to Sphinx-SimplePDF! This document provides guidelines and instructions for contributing.

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

* Python 3.10 or higher
* `uv <https://docs.astral.sh/uv/>`__ package manager

.. note::

   **Note for macOS users:** We recommend using the devcontainer for building and testing, as WeasyPrint has additional system dependencies that are easier to manage in a containerized environment.

Setting Up the Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/useblocks/sphinx-simplepdf.git
      cd sphinx-simplepdf

2. Install dependencies using uv:

   .. code-block:: bash

      uv sync --group dev

3. Install pre-commit hooks:

   .. code-block:: bash

      uv run pre-commit install

Development Workflow
--------------------

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   uv run pytest

For parallel test execution:

.. code-block:: bash

   uv run pytest -n auto

Code Quality
~~~~~~~~~~~~

This project uses several tools to maintain code quality:

* **Ruff** - Linting and formatting
* **mypy** - Static type checking
* **pre-commit** - Automated checks before commits

Running Pre-commit Manually
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   uv run pre-commit run --all-files

Running Individual Checks
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Linting
   uv run ruff check .

   # Formatting
   uv run ruff format .

   # Type checking
   uv run mypy .

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   uv sync --extra docs
   cd docs
   make html

Building a PDF (Testing the Extension)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd docs
   make simplepdf

The generated PDF will be in ``docs/_build/simplepdf/``.

Submitting Changes
------------------

Pull Request Process
~~~~~~~~~~~~~~~~~~~~

1. Fork the repository and create a new branch from ``main``
2. Make your changes
3. Ensure all tests pass and pre-commit checks succeed
4. Submit a pull request to the ``main`` branch

Commit Messages
~~~~~~~~~~~~~~~

Write clear and descriptive commit messages that explain what changes were made and why.

Code Style
~~~~~~~~~~

* Follow the existing code style in the project
* Maximum line length is 120 characters
* Use type hints where appropriate
* Keep changes focused and avoid unrelated modifications

Reporting Issues
----------------

When reporting issues, please include:

* A clear description of the problem
* Steps to reproduce the issue
* Expected vs actual behavior
* Python version and OS information
* Any relevant error messages or logs

Questions?
----------

If you have questions, feel free to open an issue on the `GitHub repository <https://github.com/useblocks/sphinx-simplepdf/issues>`__.

License
-------

By contributing to Sphinx-SimplePDF, you agree that your contributions will be licensed under the MIT License.
