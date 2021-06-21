from .settings import *
import dj_database_url

STATIC_URL = 'staticfiles'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}
