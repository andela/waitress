# -*- coding: utf-8 -*-
from django_envie.workroom import convertfiletovars

convertfiletovars()

from .base import *

DEBUG = True

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
]
