# -*- coding: utf-8 -*-
# Standard Library
import os

# Third Party Stuff
import django

from .fixtures import *  # noqa

# import pytest


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def pytest_configure(config):
    django.setup()
