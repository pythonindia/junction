# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^sync_data/$', views.sync_data, name='sync_data'),
]
