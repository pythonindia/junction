junction
========

[![Build Status](https://travis-ci.org/pythonindia/junction.svg)](https://travis-ci.org/pythonindia/junction)

Junction is a software to manage proposals, reviews, schedule, feedback during conference.

Setup
=====

Just execute these commands in your virtualenv(wrapper):

```
pip install -r requirements-dev.txt
cp settings/dev.py.sample settings/dev.py
python manage.py migrate --noinput
python manage.py sample_data
```

Initial auth data: admin/123123

Configuring Django-allauth
---------------------------

 - Go to `/admin/sites/site/` 
 - Change the default site's(the one with ID = 1) name and display to `localhost:8000`
 - Go to `Social Applications` in admin panel and add [Github](http://django-allauth.readthedocs.org/en/latest/providers.html#github) and [Google](http://django-allauth.readthedocs.org/en/latest/providers.html#google)'s auth details
