# LOCAL / DEVELOPMENT ENVIRONMENT SETTINGS
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ddtest',                      # developmentdatabase is serious; ddtest is play
        'USER': 'mapcuser',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# # Additional locations of static files
# STATICFILES_DIRS += (
#     # Put strings here, like "/home/html/static" or "C:/www/django/static".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.  <-- IN NO WAY is this best practice
#     # '/vagrant/developmentdatabase/static',
#     # '/vagrant/developmentdatabase/development/static',
# )

# TEMPLATE_DIRS += (
#     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths. <-- IN NO WAY is this best practice
#     # '/vagrant/developmentdatabase/templates',
#     # '/home/vagrant/virtualenvs/dd/lib/python2.6/site-packages/django/contrib/gis/templates',
# )

# Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.mapc.org'
EMAIL_HOST_USER = 'RSVPSender'
EMAIL_HOST_PASSWORD = 'Password1'
DEFAULT_FROM_EMAIL = 'MAPC Development Database <projections@mapc.org>'
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