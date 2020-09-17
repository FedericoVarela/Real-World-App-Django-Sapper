from .base import *

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'loggers': {
        'server': {
            'level': "WARNING"
        }
    }
}