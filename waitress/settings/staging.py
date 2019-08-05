# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv, find_dotenv
import dj_database_url

from .base import *

from .base import *

load_dotenv(find_dotenv())
STAGING_DOMAIN = os.getenv("STAGING_DOMAIN")

DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=True)}

DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql_psycopg2"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# TEMPLATES[0]["APP_DIRS"] = False
# TEMPLATES[0]["OPTIONS"]["loaders"] = [
#     (
#         "django.template.loaders.cached.Loader",
#         [
#             "django.template.loaders.filesystem.Loader",
#             "django.template.loaders.app_directories.Loader",
#             "django.template.loaders.eggs.Loader",
#         ],
#     )
# ]
#
# STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(os.environ["OPENSHIFT_REPO_DIR"], "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

ALLOWED_HOSTS = [STAGING_DOMAIN]
