# -*- coding: utf-8 -*-
import os

import django

from .fixtures import *  # noqa

# import pytest


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


def pytest_configure(config):
    django.setup()
