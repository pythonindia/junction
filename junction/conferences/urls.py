# -*- coding: utf-8 -*-

from django.urls import re_path

from . import views

urlpatterns = [re_path(r"^$", views.get_conference, name="get-conference")]
