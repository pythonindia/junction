===============
Getting Started
===============

We’re pleased that you are interested in working on Junction.

This document is meant to get you setup to work on Junction and to act as a
guide and reference to the the development setup. If you face any issues during
this process, please `open an issue`_ about it on the issue tracker.


Initial Setup
=============

Junction's development workflow is automated using `nox`_. Thus, you need
the ``nox`` command to be installed on your system. We recommend using ``pipx``
to install ``nox`` in its own isolated environment.

.. code-block:: console

   $ python -m pip install pipx
   $ pipx install nox

You will need to have a working Redis server on your system. You may
additionally want to install Postgres, although it is optional.

.. note::

   On Debian based systems, these can be installed using:

   .. code-block:: console

      $ sudo apt install redis-server postgres

Backend
-------

Create a "settings" file for local development with Django.

.. code-block:: console

   $ cp settings/dev.py.sample settings/dev.py

Create the database structure and populate it with sample data.

.. code-block:: console

   $ nox -- migrate --noinput
   $ nox -- sample_data

Admin Access
^^^^^^^^^^^^

When sample data is generated with ``nox -- sample_data``, a superuser is
created with the username ``admin`` and password ``123123``.


Frontend
--------

Working on Junction's frontend requires `NodeJS`_ and `yarn`_ to be installed on your
system. The frontend is built using `grunt`_. To setup the working
environment, run the following:

.. code-block:: console

   $ cd junction/static
   $ yarn install

Development workflow
====================

Frontend Autobuilding
---------------------

Junction has a Grunt configuration that is useful when working on the frontend.
The following command starts a build watcher which rebuilds the frontend on
every file change.

.. code-block:: console

   $ grunt

For ease of development ``app.css`` is checked in to the source code. It is not
recommended to directly make changes to ``app.css``, rather update the less files
and run ``grunt``, then commit ``app.css``

Invoking ``manage.py``
----------------------

Junction's ``nox`` configuration is set up to invoke manage.py when no other
session (i.e. ``-s ...``) is specified. This also automatically sets up an
isolated environment that contains the dependencies of Junction.

.. code-block:: console

   $ nox  # equivalent to 'python manage.py'
   $ nox -- runserver  # equivalent to 'python manage.py runserver'
   $ nox -- migrate  # equivalent to 'python manage.py migrate'

Running tests
-------------

For running the tests, run:

.. code-block:: console

   $ nox -s test

Running linters
---------------

For running the linters, run:

.. code-block:: console

   $ nox -s lint

Building documentation
----------------------

For building the documentation, run:

.. code-block:: console

   $ nox -s docs

.. _`open an issue`: https://github.com/pythonindia/junction/issues
.. _`virtualenv`: https://virtualenv.pypa.io/en/stable/
.. _`nox`: https://nox.readthedocs.io/en/stable/
.. _`NodeJS`: https://nodejs.org/
.. _`yarn`: https://yarnpkg.com/
.. _`grunt`: https://gruntjs.com/
