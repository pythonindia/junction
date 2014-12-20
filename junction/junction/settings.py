import os

from django.conf.global_settings import *  # @UnusedWildImport

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1

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
    'django.contrib.sites',
    'django.contrib.webdesign',
)

THIRD_PARTY_APPS = (
    "sendgrid",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
)

OUR_APPS = ('conferences',
            'proposals',)

INSTALLED_APPS = CORE_APPS + THIRD_PARTY_APPS + OUR_APPS

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

ROOT_URLCONF = 'junction.urls'
WSGI_APPLICATION = 'junction.wsgi.application'

TIME_ZONE = 'Asia/Kolkata'
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets', 'collected-static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets', 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
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


#Email Settings - django-sendgrid
SENDGRID_EMAIL_HOST = "smtp.sendgrid.net"
SENDGRID_EMAIL_PORT = 587
SENDGRID_EMAIL_USERNAME = os.environ.get('SENDGRID_USERNAME', ''),
SENDGRID_EMAIL_PASSWORD = os.environ.get('SENDGRID_PASSWORD', ''),
SENDGRID_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', ''),


#setup dynamic hostname for logging
import socket
HOSTNAME = socket.gethostname()

#ensure log files can be created if path doesn't exist
def log_file(dir, file):
    dir = os.path.expanduser(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return os.path.join(dir, file)

LOG_DIR = os.path.join(BASE_DIR, "logs")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
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
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': log_file(LOG_DIR,'error.log'),
        },
        
    },
    'loggers': {
       'django.request': {
            'handlers': ['mail_admins','file'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Uncomment following to turn on sql logging
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        
        'app_log': {
            'handlers': ['console','mail_admins','file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


# Dev Settings
try:
    from junction.dev import *  # @UnusedWildImport
except ImportError:
    pass
