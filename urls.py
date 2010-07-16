from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^communitycomments/', include('communitycomments.foo.urls')),
    (r'^$', 'communitycomments.projects.views.index'),
    (r'^(?P<community_name>\w+)/$', 'communitycomments.projects.views.community'),
    (r'^project/(?P<project_id>\d+)/$', 'communitycomments.projects.views.detail'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
