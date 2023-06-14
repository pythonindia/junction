===============
Getting Started
===============

We’re pleased that you are interested in working on Junction.

This document is meant to get you setup to work on Junction and to act as a
guide and reference to the the development setup. If you face any issues during
this process, please `open an issue`_ about it on the issue tracker.


Initial Setup
=============

Junction's development workflow is automated using Docker with docker-compose.
We also use Docker for production deployment.

To setup Docker and docker-compose locally follow the `Docker Getting started`_ doc.

After Docker and docker-compose is setup locally follow these steps

.. code-block:: console

   $ cp .env.sample .env
   $ docker-compose build
   $ docker-compose up -d

This will build and run the application after running database migrations

Access the application at https://localhost:8888

Backend
--------

Populate Database with sample data 

.. code-block:: console

   $ docker-compose exec web /bin/sh
   # python manage.py sample_data

Admin Access
^^^^^^^^^^^^

When sample data is generated, a superuser is created with the username ``admin`` and password ``123123``.
Go to https://localhost:8888/nimda to access Django Admin Panel


Development workflow
====================

Running tests
-------------

For running the tests, run:

.. code-block:: console

   $ docker-compose -f docker-compose.test.yml up -d

Running linters
---------------

We use `pre-commit`_ for linting. Install pre-commit then run:

.. code-block:: console

   $ pre-commit install

This will install all linters in form of git hooks. To manually run the linter run:

.. code-block:: console

   $ pre-commit run --all-files

Building documentation
----------------------

For building the documentation, run:

.. code-block:: console

   $ python -m pip install -r tools/requirements-docs.txt
   $ cd docs
   $ make html

.. _`open an issue`: https://github.com/pythonindia/junction/issues
.. _`Docker Getting started`: https://www.docker.com/get-started
.. _`pre-commit`: https://pre-commit.com/
