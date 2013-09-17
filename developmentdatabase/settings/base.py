# BASE SETTINGS COMMON TO ALL ENVIRONMENTS
import os, sys, dj_database_url
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

abspath = lambda *p: os.path.abspath(os.path.join(*p))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# print("PROJECT ROOT")
# print(PROJECT_ROOT)

ADMINS = (
    ('Matt Cloyd', 'mapc@mapc.org'),
)
MANAGERS = ADMINS

# The current environment. Set the environment variable ENV_TYPE in each environment
# to one of: [local, staging, production].
# TODO: DJANGO_SETTINGS_MODULE = eval(developmentdatabase.settings.#{get_env_variable("ENV_TYPE")})

DJANGO_SETTINGS_MODULE = get_env_variable("ENV_TYPE_FULL")
SECRET_KEY   = get_env_variable("SECRET_KEY")
BING_API_KEY = get_env_variable("BING_API_KEY")
WSAPIKEY     = get_env_variable("WSAPIKEY")


DATABASES = {}
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = abspath(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages', # flash
    'developmentdatabase.context_processors.template_settings',
    'tim.context_processors.auth_variables',)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # required to be listed before flash
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', # flash
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'developmentdatabase.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'developmentdatabase.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'grappelli',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
    # 3rd party
    'userena',
    'guardian',
    'easy_thumbnails',
    'reversion',
    'profiles',
    'bootstrap',
    'tastypie',

    # project
    'development',
    'tim',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# flash
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# tastypie
API_LIMIT_PER_PAGE = 20

# Userena
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# TODO: Why are these set here? Why is this not in URLConfs?
AUTH_PROFILE_MODULE = 'profiles.Profile'
LOGIN_REDIRECT_URL = '/projects/search/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
USERENA_MUGSHOT_GRAVATAR = False
USERENA_MUGSHOT_DEFAULT = STATIC_URL + 'img/mugshot.png'
USERENA_DISABLE_PROFILE_LIST = True
USERENA_HIDE_EMAIL = True

# Guardian
ANONYMOUS_USER_ID = -1

# WalkScore API
WS_MORE_INFO_ICON = 'http://www2.walkscore.com/images/api-more-info.gif'
WS_MORE_INFO_LINK = 'http://www.walkscore.com/how-it-works.shtml'
WS_LOGO_URL = 'http://www2.walkscore.com/images/api-logo.gif'

