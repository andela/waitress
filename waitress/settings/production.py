# -*- coding: utf-8 -*-
import dj_database_url
from dotenv import load_dotenv, find_dotenv

from .base import *

load_dotenv(find_dotenv())
PRODUCTION_DOMAIN = os.getenv("PROD_DOMAIN")

DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}

DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql_psycopg2"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = [PRODUCTION_DOMAIN]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
