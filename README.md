junction
========

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/pythonindia/junction?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/pythonindia/junction.svg)](https://travis-ci.org/pythonindia/junction)

Junction is a software to manage proposals, reviews, schedule, feedback during conference.

Setup
=====

It is advised to install all the requirements inside [virtualenv](https://virtualenv.pypa.io/en/latest/), use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) to manage virtualenvs.

```
pip install -r requirements-dev.txt
cp settings/dev.py.sample settings/dev.py
python manage.py migrate --noinput
python manage.py sample_data
python manage.py createsuperuser (Use this user for login)
```

Initial auth data: admin/123123

Configuring Django-allauth
---------------------------

 - Go to `/admin/sites/site/` 
 - Change the default site's(the one with ID = 1) name and display to `localhost:8000`
 - Go to `Social Applications` in admin panel and add [Github](http://django-allauth.readthedocs.org/en/latest/providers.html#github) and [Google](http://django-allauth.readthedocs.org/en/latest/providers.html#google)'s auth details
