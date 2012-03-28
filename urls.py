from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from django.views.generic import TemplateView



# from django.views.generic.simple import direct_to_template

from registration.views import register

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# API
from tastypie.api import Api
from projects.api import ProjectResource

v1_api = Api(api_name='v1')
v1_api.register(ProjectResource())



urlpatterns = patterns('',
    # Example:
    url(r'^$', 'projects.views.index', name='home'),

    
    # ('^project/filter/$', TemplateView.as_view(template_name='projects/filter.html')),
    ('^project/filter/$', 'projects.views.filter'),
    
    (r'^project/(?P<project_id>\d+)/$', 'projects.views.detail'),
    (r'^project/(?P<project_id>\d+)/edit/$', 'projects.views.edit'),
    (r'^project/add/$', 'projects.views.add'),
    # (r'^project/(?P<project_id>\d+)/save/$', 'communitycomments.projects.views.save'),
    (r'^project/(?P<project_id>\d+)/geojson/$', 'projects.views.project_geojson'),
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # API
    (r'^api/', include(v1_api.urls)),
    
    
    (r'^accounts/', include('accounts.urls')),
    
    # Filter by community name
    (r'^(?P<town_name>\w+)/taz/geojson/$', 'projects.views.town_taz_geojson'),
    (r'^(?P<town_name>\w+)/$', 'projects.views.community'),
    # (r'^(?P<community_name>\w+)/$', 'communitycomments.projects.views.community')
    # (r'^game', direct_to_template,
    #        { 'template': 'game.html' }, 'game'    ),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
