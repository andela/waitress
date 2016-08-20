# -*- coding: utf-8 -*-
from .base import *
import dj_database_url

PRODUCTION_DOMAIN = 'waitressandela.herokuapp.com'

DEBUG = True

DATABASES = {
    'default': dj_database_url.config()
}

DATABASES['default']['ENGINE'] = 'django_postgrespool'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = [PRODUCTION_DOMAIN]
