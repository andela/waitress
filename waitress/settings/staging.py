# -*- coding: utf-8 -*-
import os
import urlparse

from dotenv import load_dotenv, find_dotenv

from .base import *


load_dotenv(find_dotenv())
STAGING_DOMAIN = os.getenv("STAGING_DOMAIN")

db_url = urlparse.urlparse(os.environ.get("OPENSHIFT_POSTGRESQL_DB_URL"))
DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["OPENSHIFT_APP_NAME"],
        "USER": db_url.username,
        "PASSWORD": db_url.password,
        "HOST": db_url.hostname,
        "PORT": db_url.port,
    }
}

DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql_psycopg2"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = ["*"]

LOG_DIR = os.environ.get("OPENSHIFT_LOG_DIR")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "django.log"),
        }
    },
    "loggers": {
        "django.request": {"handlers": ["file"], "level": "WARNING", "propagate": True}
    },
}


TEMPLATES[0]["APP_DIRS"] = False
TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
            "django.template.loaders.eggs.Loader",
        ],
    )
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.environ["OPENSHIFT_REPO_DIR"], "static")
STATICFILES_STORAGE = None

ALLOWED_HOSTS = [STAGING_DOMAIN]
