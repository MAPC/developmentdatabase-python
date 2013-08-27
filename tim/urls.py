from django.conf.urls import patterns, include, url
# from django.views.generic import TemplateView

from tim import views


urlpatterns = patterns('tim.views',
    url('^(?P<municipality>\w+)/$', 'municipality', name='municipality'),
    url('^all/',                     'all',          name='all'),
)