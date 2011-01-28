import os, sys
sys.path.append('C:/dev/django')
os.environ['DJANGO_SETTINGS_MODULE'] = 'projections.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()