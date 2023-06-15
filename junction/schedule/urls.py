# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import re_path

from . import views

urlpatterns = [
    # schedule urls
    re_path(r"^dummy_schedule/$", views.dummy_schedule, name="dummy_schedule"),
]
