# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import os

# Third Party Stuff
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('junction')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
