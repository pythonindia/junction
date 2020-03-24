# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings


def site_info(request):
    return {"SITE_INFO": settings.SITE_VARIABLES}
