import os

from django.conf.global_settings import *  # noqa
from django.utils.translation import ugettext_lazy as _

# Standard Library
from os.path import dirname, join

# Build paths inside the project like this: os.path.join(ROOT_DIR, ...)
ROOT_DIR = dirname(dirname(__file__))
APP_DIR = join(ROOT_DIR, 'junction')

SITE_ID = 1

ADMINS = (
    ('Bibhas', 'me@bibhas.in'),
    ('Kracekumar', 'me@kracekumar.com'),
    ('Sivabramaniam Arunachalam', 'siva@sivaa.in'),
)

# Absolute Url of frontend hosted site. Used to render the urls in templattes,
# static and media files appropriately. e.g 'https://in.pycon.org/junction'
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')

# General project information
# These are available in the template as SITE_INFO.<title>
SITE_VARIABLES = {
    'site_name': 'Junction',
    'site_description': 'Junction is a software to manage proposals, reviews, schedule, feedback during conference.',
    'google_analytics_id': os.environ.get('GOOGLE_ANALYTICS_ID', None),
    'site_url': SITE_URL,
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORE_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.webdesign',
)

THIRD_PARTY_APPS = (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',

    'bootstrap3',

    'pagedown',
    'django_markdown',
    'django_bootstrap_breadcrumbs',
)

OUR_APPS = (
    'junction.base',
    'junction.conferences',
    'junction.proposals',
    'junction.pages',
)

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + OUR_APPS

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    "junction.base.context_processors.site_info",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[{}] ".format(SITE_VARIABLES['site_name'])
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
LOGIN_REDIRECT_URL = '/'

# E-Mail Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', ''),
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', ''),
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SITE_VARIABLES['site_name'] + ' <noreply@pssi.org.in>'

BOOTSTRAP3 = {
    'required_css_class': 'required',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', ],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['file', ],
        },
    }
}

LANGUAGES = (
    ("en", _("English")),
)


ROOT_URLCONF = 'junction.urls'
WSGI_APPLICATION = 'wsgi.application'

ATOMIC_REQUESTS = True
TIME_ZONE = 'Asia/Kolkata'
LANGUAGE_CODE = "en"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(APP_DIR, 'assets', 'collected-static')
STATICFILES_DIRS = (
    os.path.join(APP_DIR, 'static'),
)

MEDIA_ROOT = join(ROOT_DIR, '.media')
MEDIA_URL = '/m/'

TEMPLATE_DIRS = (
    os.path.join(APP_DIR, 'templates'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

SECRET_KEY = os.environ.get('SECRET_KEY', 'z^bd9lk)o!03n#9e_u87zidd1zt7*^_oc4v6t!@@86vtbu0*&j')

DEBUG = TEMPLATE_DEBUG = os.environ.get('DEBUG', 'on') == 'on'

ALLOWED_HOSTS = []  # TODO:

SITE_PROTOCOL = 'http'

MARKDOWN_EXTENSIONS = ['linkify']


# twitter settings
CONSUMER_KEY = os.environ.get('CONSUMER_KEY', '')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET', '')
ACCESS_TOKEN_KEY = os.environ.get('ACCESS_TOKEN_KEY', '')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET', '')
