from django.conf.urls import patterns, include, url
# from django.views.generic import TemplateView

from development import views


urlpatterns = patterns('development.views',
    url('^$', 'projects_geojson'),
    url('^csv/', 'projects_csv', name='projects_csv'),
    url('^search/', 'search', name='search'),
    url('^detail/(?P<dd_id>\d+)/$', 'detail', name='detail'),
    url('^update/(?P<dd_id>\d+)/$', 'update', name='update'),
    url('^add/', 'add', name='add'),
)