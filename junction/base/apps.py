from __future__ import print_function

import sys

from django.apps import AppConfig

from . import monkey


class BaseAppConfig(AppConfig):
    name = "junction.base"
    verbose_name = "Base App Config"

    def ready(self):
        print("Monkey patching...", file=sys.stderr)
        monkey.patch_urltag()
        monkey.patch_urlresolvers()
