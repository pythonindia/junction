# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import os
from os.path import dirname, join

from django.utils.translation import gettext_lazy as _


DEBUG = os.environ.get("DEBUG", False)
# Build paths inside the project like this: os.path.join(ROOT_DIR, ...)
ROOT_DIR = dirname(dirname(__file__))
APP_DIR = join(ROOT_DIR, "junction")


DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


ADMINS = ()


# Absolute Url of frontend hosted site. Used to render the urls in templattes,
# static and media files appropriately. e.g 'https://in.pycon.org/junction'
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")

# General project information
# These are available in the template as SITE_INFO.<title>
dt = datetime.datetime.now()
SITE_VARIABLES = {
    "site_name": os.environ.get("SITE_NAME", "Junction"),
    "site_description": "Junction is a software to manage proposals, reviews, schedule, feedback during conference.",
    "google_analytics_id": os.environ.get("GOOGLE_ANALYTICS_ID", None),
    "site_url": SITE_URL,
    "footer": "&copy; {} • Python Software Society of India".format(dt.year),
    # Enables Facebook sharing of proposals
    "facebook_app_id": os.environ.get("FACEBOOK_APP_ID", None),
}

MIDDLEWARE = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
)

CORE_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
)

THIRD_PARTY_APPS = (
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    "bootstrap3",
    "pagedown",
    "markdown_deux",
    "django_bootstrap_breadcrumbs",
    "rest_framework",
    "django_filters",
    "simple_history",
    # "sslserver", used in development server only
)

OUR_APPS = (
    "junction.base",
    "junction.conferences",
    "junction.proposals",
    "junction.schedule",
    "junction.profiles",
    "junction.devices",
    "junction.tickets",
    "junction.feedback",
)

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + OUR_APPS
SITE_ID = 1

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        # For each provider, you can choose whether or not the
        # email address(es) retrieved from the provider are to be
        # interpreted as verified.
        'VERIFIED_EMAIL': True,
        'APP': {
            'client_id': 'enter your github client_id',
            'secret': 'enter your github secret key',
            'key': '',
        },
    },
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'SCOPE': {
            'profile',
            'email',
        },
        'APP': {
            'client_id': 'enter your gogole oauth client_id',
            'secret': 'enter your google oauth secret ',
            'key': '',
        },
    }
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(APP_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "junction.base.context_processors.site_info",
                "django.contrib.messages.context_processors.messages",
            ],
            "debug": DEBUG,
        },
    },
]


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[{}] ".format(SITE_VARIABLES["site_name"])
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
EMAIL_SUBJECT_PREFIX = ACCOUNT_EMAIL_SUBJECT_PREFIX

LOGIN_REDIRECT_URL = "/"

# E-Mail Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = (os.environ.get("EMAIL_HOST_USER", "enter gmail id"),)
# turn on 2-step verification in your gmail account and add App password
EMAIL_HOST_PASSWORD = (os.environ.get("EMAIL_HOST_PASSWORD", "enter App password"),)
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = SITE_VARIABLES["site_name"] + " <noreply@pssi.org.in>"

BOOTSTRAP3 = {
    "required_css_class": "required",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins", ],
            "level": "ERROR",
            "propagate": True,
        },
        "django.db.backends": {"level": "DEBUG", "handlers": ["file", ], },
    },
}

LANGUAGES = (("en", _("English")),)


ROOT_URLCONF = "junction.urls"
WSGI_APPLICATION = "wsgi.application"

ATOMIC_REQUESTS = True
TIME_ZONE = "Asia/Kolkata"
LANGUAGE_CODE = "en"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(APP_DIR, "assets", "collected-static")
STATICFILES_DIRS = (os.path.join(APP_DIR, "static"),)

MEDIA_ROOT = join(ROOT_DIR, ".media")
MEDIA_URL = "/m/"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB", "junction"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "junction"),
        "HOST": os.environ.get("HOST_NAME", "db"),
        "PORT": os.environ.get("PORT", "5432"),
    }
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "z^bd9lk)o!03n#9e_u87zidd1zt7*^_oc4v6t!@@86vtbu0*&j"
)


ALLOWED_HOSTS = ["*"]

SITE_PROTOCOL = "http"

# MARKDOWN_EXTENSIONS = ['linkify']


# twitter settings
TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY", None)
TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET", None)
TWITTER_ACCESS_TOKEN_KEY = os.environ.get("TWITTER_ACCESS_TOKEN_KEY", None)
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", None)

# Add connection life time
# Make sure DB request held on for minimim 5 minutes
CONN_MAX_AGE = 300

# REST_FRAMEWORK = {
#     "DEFAULT_FILTER_BACKENDS": ("rest_framework.filters.DjangoFilterBackend",)
# }

EXPLARA_API_TOKEN = "shjbalkfbdskjlbdskljbdskaljfb"

QR_CODES_DIR = ROOT_DIR + "/qr_files"

USE_ASYNC_FOR_EMAIL = os.environ.get("USE_ASYNC_FOR_EMAIL", False)

USER_SPAM_THRESHOLD = 2

SPAM_MODERATION_ADMINS = []


ENABLE_SECOND_PHASE_VOTING = False
ENABLE_UPLOAD_CONTENT = False
