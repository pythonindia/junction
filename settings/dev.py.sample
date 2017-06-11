# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from .common import *  # noqa

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    }
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.debug",
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += ('django_extensions',)

# settings for celery
BROKER_URL = os.environ.get("BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", 'redis://127.0.0.1:6379/0')

SPAM_MODERATION_ADMINS = []
