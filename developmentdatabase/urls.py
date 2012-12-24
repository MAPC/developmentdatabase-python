from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from profiles.forms import SignupFormExtra


# API
from tastypie.api import Api
from developmentdatabase.api import ProjectResource, MuniResource, ProjectStatusResource

v1_api = Api(api_name='v1')
v1_api.register(ProjectResource())
v1_api.register(MuniResource())
v1_api.register(ProjectStatusResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dd_new.views.home', name='home'),
    # url(r'^dd_new/', include('dd_new.foo.urls')),
    url('^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url('^$', TemplateView.as_view(template_name='development/filter.html'), name='project_filter'),
    
    (r'^projects/', include('development.urls')),    

    # API
    (r'^api/', include(v1_api.urls)),

    # Userena
    # Override the signup form
    (r'^accounts/signup/$', 'userena.views.signup', {'signup_form': SignupFormExtra}),
    (r'^accounts/', include('userena.urls')),

    # grappelli admin interface
    (r'^grappelli/', include('grappelli.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
)
