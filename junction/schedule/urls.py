# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf.urls import include, patterns, url

from . import views

urlpatterns = patterns(
    '',
    # schedule urls
    url(r'^dummy_schedule/$', views.dummy_schedule, name='dummy_schedule'),
)
