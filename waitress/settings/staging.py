# -*- coding: utf-8 -*-
import os
from .base import *
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}


DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

LOG_DIR = os.environ.get('OPENSHIFT_LOG_DIR')

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'file': {
      'level': 'WARNING',
      'class': 'logging.FileHandler',
      'filename': os.path.join(LOG_DIR, 'django.log'),
    },
  },
  'loggers': {
    'django.request': {
      'handlers': ['file'],
      'level': 'WARNING',
      'propagate': True,
    },
  },
}

STATIC_ROOT = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'static')

TEMPLATES[0]['APP_DIRS'] = False
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader'
    ]),
]

STATICFILES_STORAGE = None
