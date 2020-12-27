from .base import *
from datetime import timedelta

ALLOWED_HOSTS = ["FedericoVarela.pythonanywhere.com"]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
CORS_ALLOW_ALL_ORIGINS = True

# Disable the browsable API
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=15)