# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # schedule urls
    url(r'^dummy_schedule/$', views.dummy_schedule, name='dummy_schedule'),
]
