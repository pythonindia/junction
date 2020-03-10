Getting Started
===============

We’re pleased that you are interested in working on Junction.

This document is meant to get you setup to work on Junction and to act as a
guide and reference to the the development setup. If you face any issues during
this process, please `open an issue`_ about it on the issue tracker.


Development environment setup
*****************************

You should create a virtual environment to isolate your development environment
from the system, when developing Junction. This is usually done by creating
`virtualenv`_.

.. Update this section when we do adopt ``pipenv`` for our environment
   management needs.

You will need to have a working Redis server on your system. You may
additionally need PostgreSQL and TCL as well.

.. note::
   On Debian based systems, these can be installed using:

   .. code-block:: console

      $ sudo apt-get install redis-server libpq-dev tcl

Create a virtual environment, to isolate the development environment from the
system. This can be done by using `virtualenv`_:

.. code-block:: console

      $ python -m virtualenv env

After activating a virtual environment, install all packages required for
development. They are listed in ``requirements-dev.txt`` and can be installed
using:

.. code-block:: console

   $ pip install -r requirements-dev.txt


Backend Development
*******************

Create a "settings" file for local development with Django.

.. code-block:: console

   $ cp settings/dev.py.sample settings/dev.py

With the virtualenv activated, create the database structure and populate it
with sample data.

.. code-block:: console

   $ python manage.py migrate --noinput
   $ python manage.py sample_data

Local Admin Access
------------------

When sample data is generated with ``manage.py sample_data``, a superuser is
created with the username ``admin`` and password ``123123``.


Frontend development
********************

Working on Junction's frontend requires `NodeJS`_ to be installed on your
system. The frontend is built using `bower`_ and `grunt`_. To setup the working
environment, run the following:

.. code-block:: console

   $ cd junction/static
   $ npm install
   $ bower install

Once setup, a build watcher is available, that rebuilds the frontend, every time
a change is made to the frontend code. This can be run using:

.. code-block:: console

   $ grunt


Building documentation
**********************

For building the documentation, run:

.. code-block:: console

   $ cd docs
   $ make html

.. _`open an issue`: https://github.com/pythonindia/junction/issues
.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/
.. _`NodeJS`: https://nodejs.org/
.. _`bower`: https://bower.io/
.. _`grunt`: https://gruntjs.com/
