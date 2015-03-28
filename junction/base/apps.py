# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Standard Library
import sys

# Third Party Stuff
from django.apps import AppConfig

from . import monkey


class BaseAppConfig(AppConfig):
    name = "junction.base"
    verbose_name = "Base App Config"

    def ready(self):
        print("Monkey patching...", file=sys.stderr)
        monkey.patch_urltag()
        monkey.patch_urlresolvers()
