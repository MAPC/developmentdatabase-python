from django.conf.urls import patterns, include, url
# from django.views.generic import TemplateView

from tim import views


urlpatterns = patterns('tim.views',
    url('^all/',                         'all',          name='all'),
    url('^(?P<municipality_name>\w+)/$', 'municipality', name='municipality'),
)