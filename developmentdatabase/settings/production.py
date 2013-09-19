# PRODUCTION ENVIRONMENT SETTINGS
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

dummy   = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_BACKEND   = dummy

EMAIL_USE_TLS       = True
EMAIL_HOST          = 'mail.mapc.org'
EMAIL_HOST_USER     = 'RSVPSender'
EMAIL_HOST_PASSWORD = 'Password1'
DEFAULT_FROM_EMAIL  = 'MAPC Development Database <projections@mapc.org>'
EMAIL_PORT = 25

# Userena
USERENA_ACTIVATION_REQUIRED = False

INSTALLED_APPS += (
    'south',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']