# -*- coding: utf-8 -*-
# Copyright (C) 2020-2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=line-too-long, invalid-name

import os

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

DEBUG = 0  # no debug output as default

ENV_HOSTS = os.environ.get("ALLOWED_HOSTS")

# If not running in docker, use empty array
if ENV_HOSTS is not None:
    ALLOWED_HOSTS = ENV_HOSTS.split(" ")
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'graphene_django',
    'selene',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # XFrameOptionsMiddleware is used set the X-Frame-Options to DENY
    # this header MUST be set in nginx for production
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hyperion.urls'

WSGI_APPLICATION = 'hyperion.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT is required for python manage.py collectstatic
# Which is needed to use this module with nginx
STATIC_ROOT = BASE_DIR / 'static'

# Gets GMP_SOCKET_PATH from .selene.dev
# If not running in docker use your gvmd.sock path
SELENE = {
    'GMP_SOCKET_PATH': os.environ.get(
        "GMP_SOCKET_PATH", '/var/run/gvmd.sock'  # add your gvmd.sock path here
    )
}

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

# session timeout in seconds (15 min)
SESSION_COOKIE_AGE = 900

# use pickle as serializer to allow seralizing of datetime for session expiry
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# always try to use secret key from the environment
SECRET_KEY = os.environ.get("SECRET_KEY")

# fallback to read the key from file
if not SECRET_KEY:
    _secret_key_file = BASE_DIR / 'secret.key'
    if _secret_key_file.exists():
        SECRET_KEY = _secret_key_file.read_text()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ]
        },
    }
]
