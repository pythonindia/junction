# -*- coding: utf-8 -*-
# Standard Library
import os

# Third Party Stuff
import django
# import pytest

from .fixtures import *  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def pytest_configure(config):
    django.setup()
