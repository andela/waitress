# -*- coding: utf-8 -*-
import os
from os.path import join, dirname

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

from .base import *

DEBUG = True

INSTALLED_APPS += ("django_nose",)

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

NOSE_ARGS = ["--with-coverage"]

ALLOWED_HOSTS = ["*"]

# configure your database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": os.getenv(
            "DB_NAME", "waitress"
        ),  # Or path to database file if using sqlite3.
        "USER": os.getenv("DB_USER"),  # Not used with sqlite3.
        "PASSWORD": os.getenv("DB_PASSWORD"),  # Not used with sqlite3.
        "HOST": "localhost",  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "5432",  # Set to empty string for default. Not used with sqlite3.
    }
}
