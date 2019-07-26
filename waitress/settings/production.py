# -*- coding: utf-8 -*-
from .base import *
import dj_database_url

PRODUCTION_DOMAIN = "waitressandela.herokuapp.com"
STAGING_DOMAIN = "waitress-staging.herokuapp.com"

DEBUG = True

DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}

DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql_psycopg2"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = [PRODUCTION_DOMAIN, STAGING_DOMAIN]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
