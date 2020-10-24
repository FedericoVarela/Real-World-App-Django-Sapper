from .base import *

ALLOWED_HOSTS = ["FedericoVarela.pythonanywhere.com"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
CORS_ALLOW_ALL_ORIGINS = True

LOGGING = {
    'version': 1,
    'loggers': {
        'server': {
            'level': "WARNING"
        }
    }
}

# Disable the browsable API
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)
