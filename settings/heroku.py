import dj_database_url

DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = ['*']

DEGUG = False
