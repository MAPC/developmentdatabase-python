from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# API
from tastypie.api import Api
from development.api import ProjectResource, MuniResource

v1_api = Api(api_name='v1')
v1_api.register(ProjectResource())
v1_api.register(MuniResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dd_new.views.home', name='home'),
    # url(r'^dd_new/', include('dd_new.foo.urls')),
    url('^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url('^$', TemplateView.as_view(template_name='development/filter.html'), name='project_filter'),
    
    (r'^projects/', include('development.urls')),    

    # API
    (r'^api/', include(v1_api.urls)),

    # grappelli admin interface
    (r'^grappelli/', include('grappelli.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
