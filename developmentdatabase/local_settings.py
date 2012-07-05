from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Christian Spanring', 'cspanring@mapc.org'),
)

TIME_ZONE = 'America/New_York'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'developmentdatabase',                      # Or path to database file if using sqlite3.
        'USER': 'django',                      # Not used with sqlite3.
        'PASSWORD': 'django',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kdaubjft_@glmm5go2@=^=^qwv_@-$%!bp-72b_#-hn$&amp;1!!68'

# Additional locations of static files
STATICFILES_DIRS += (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/vagrant/dd_new/static',
    '/vagrant/dd_new/development/static',
)

TEMPLATE_DIRS += (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/vagrant/dd_new/templates',
    '/home/vagrant/virtualenvs/dd-new/lib/python2.6/site-packages/django/contrib/gis/templates',
)

INSTALLED_APPS += (
    'south',
)

# FIXME: add better security for key
BING_API_KEY = 'An8pfp-PjegjSInpD2JyXw5gMufAZBvZ_q3cbJb-kWiZ1H55gpJbxndbFHPsO_HN'