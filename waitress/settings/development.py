# -*- coding: utf-8 -*-
from django_envie.workroom import convertfiletovars

convertfiletovars()

import dj_database_url

from .base import *

DEBUG = True

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
]

DATABASES = {
    'default': dj_database_url.config()
}

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
