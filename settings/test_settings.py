# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from .common import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'test.sqlite3'),
    }
}

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.debug",
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ('django_extensions',)

DEVICE_VERIFICATION_CODE = 11111
