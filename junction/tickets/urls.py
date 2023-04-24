# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^sync_data/$", views.sync_data, name="sync_data"),
]
