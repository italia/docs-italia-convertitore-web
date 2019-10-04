# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "v7i$il9kdkgtxq3-t^&iajg2ms*v+7&9u2=pde=$a-j($ibyvo"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "docs_italia_convertitore_web",
    "tests.test_app",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

SITE_ID = 1

PRODUCTION_DOMAIN = 'http://convert.com'
MEDIA_URL = 'http://convert.com/media/'
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

PREMAILER_ALLOW_NETWORK = False
