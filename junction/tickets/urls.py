# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf.urls import patterns, url

# Junction Stuff
from . import views

urlpatterns = patterns(
    '',
    url(r'^sync_data/$', views.sync_data, name='sync_data'),
)
