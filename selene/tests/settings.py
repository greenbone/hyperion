SECRET_KEY = 'fake-key'

INSTALLED_APPS = ['graphene_django']

MIDDLEWARE = ['django.contrib.sessions.middleware.SessionMiddleware']

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'gvmd'}
}

ROOT_URLCONF = 'selene.urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'null': {'class': 'logging.NullHandler'}},
    'loggers': {'graphql.execution': {'handlers': ['null'], 'level': 'NOTSET'}},
}

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

# use pickle as serializer to allow seralizing of datetime for session expiry
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# 5 minutes
SESSION_COOKIE_AGE = 300
