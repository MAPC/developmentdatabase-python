from django.conf.urls.defaults import *

# from django.views.generic.simple import direct_to_template

from registration.views import register

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
	url(r'^$', 'communitycomments.projects.views.index', name='home'),
    
    (r'^project/(?P<project_id>\d+)/$', 'communitycomments.projects.views.detail'),
    (r'^project/(?P<project_id>\d+)/edit/$', 'communitycomments.projects.views.edit'),
	(r'^project/add/$', 'communitycomments.projects.views.add'),
    # (r'^project/(?P<project_id>\d+)/save/$', 'communitycomments.projects.views.save'),
    (r'^project/(?P<project_id>\d+)/geojson/$', 'communitycomments.projects.views.project_geojson'),
    
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    
    
    
    
    (r'^accounts/', include('communitycomments.accounts.urls')),
    
    # Filter by community name
    (r'^(?P<town_name>\w+)/taz/geojson/$', 'communitycomments.projects.views.town_taz_geojson'),
    (r'^(?P<town_name>\w+)/$', 'communitycomments.projects.views.community'),
    # (r'^(?P<community_name>\w+)/$', 'communitycomments.projects.views.community')
	# (r'^game', direct_to_template,
    #        { 'template': 'game.html' }, 'game'	),
)
