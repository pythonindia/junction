junction
========

Junction is a software to manage proposals, reviews, schedule, feedback during conference.

Setup
=====

- Clone the repository `git clone git@github.com:pythonindia/junction.git` or `git clone https://github.com/pythonindia/junction.git`
- Create a virtualenv called `junction`
- Install the dependencies `pip install -r requirements-dev.txt`
- Create the dev settings file from `dev.py.sample`
- Run `python manage.py migrate` to apply pending migrations
- Run `python manage.py runserver` to start the dev server

Initial Data
------------
- Create `Conference` and related information using django admin.

Configuring Django-allauth
---------------------------

 - Go to `/admin/sites/site/` 
 - Change the default site's(the one with ID = 1) name and display to `localhost:8000`
 - Go to `Social Applications` in admin panel and add [Github](http://django-allauth.readthedocs.org/en/latest/providers.html#github) and [Google](http://django-allauth.readthedocs.org/en/latest/providers.html#google)'s auth details
