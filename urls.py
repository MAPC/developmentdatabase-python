from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
	url(r'^$', 'communitycomments.projects.views.index', name='home'),

    (r'^project/(?P<project_id>\d+)/$', 'communitycomments.projects.views.detail'),
    (r'^project/(?P<project_id>\d+)/edit/$', 'communitycomments.projects.views.edit'),
    # (r'^project/(?P<project_id>\d+)/save/$', 'communitycomments.projects.views.save'),
    (r'^project/(?P<project_id>\d+)/geojson/$', 'communitycomments.projects.views.geojson'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Filter by community name
    (r'^(?P<community_name>\w+)/$', 'communitycomments.projects.views.community'),
    (r'^(?P<community_name>\w+)/$', 'communitycomments.projects.views.community')
	# (r'^game', direct_to_template,
    #        { 'template': 'game.html' }, 'game'	),
)
