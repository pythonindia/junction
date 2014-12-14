import os

from django.conf.global_settings import *  # @UnusedWildImport

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
)

OUR_APPS = ('conferences',
           'proposals',
)

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + OUR_APPS


ROOT_URLCONF = 'junction.urls'
WSGI_APPLICATION = 'junction.wsgi.application'

TIME_ZONE = 'UTC'
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
