# -*- coding: utf-8 -*-
from .base import *
import urlparse
import os


db_url = urlparse.urlparse(os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'))
DEBUG = False

DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.environ['OPENSHIFT_APP_NAME'],
    'USER': db_url.username,
    'PASSWORD': db_url.password,
    'HOST': db_url.hostname,
    'PORT': db_url.port,
}
}

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']
