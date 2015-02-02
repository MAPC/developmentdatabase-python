# LOCAL / DEVELOPMENT ENVIRONMENT SETTINGS
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

to_file = 'django.core.mail.backends.filebased.EmailBackend'
dummy   = 'django.core.mail.backends.dummy.EmailBackend'

EMAIL_BACKEND   = to_file
EMAIL_FILE_PATH = abspath(PROJECT_ROOT, 'sent_mail')

EMAIL_USE_TLS       = True
EMAIL_HOST          = 'mail.mapc.org'
EMAIL_HOST_USER     = 'RSVPSender'
EMAIL_HOST_PASSWORD = 'Password1'
DEFAULT_FROM_EMAIL  = 'MAPC Development Database <projections@mapc.org>'
EMAIL_PORT = 25

# Userena
USERENA_ACTIVATION_REQUIRED = False

# send_mail('Subject here', 'Here is the message.', 'projections@mapc.org', ['cspanring@mapc.org'], fail_silently=False)

DEBUG_TOOLBAR = DEBUG
if DEBUG_TOOLBAR:
    INTERNAL_IPS = ('127.0.0.1','10.0.2.2')
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.version.VersionDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )
    INSTALLED_APPS += ('debug_toolbar',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

INSTALLED_APPS += (
    'south',
    'debug_toolbar',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']