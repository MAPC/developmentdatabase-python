from django.conf.urls import patterns, include, url
# from django.views.generic import TemplateView

from development import views


urlpatterns = patterns('development.views',
    # Examples:
    # url(r'^$', 'dd_new.views.home', name='home'),
    # url(r'^dd_new/', include('dd_new.foo.urls')),
    # url('^$', TemplateView.as_view(template_name='index.html'), name='home'),
    # url('^filter/', TemplateView.as_view(template_name='development/filter.html'), name='project_filter'),
    url('^filter/', 'filter', name='filter'),
    url('^detail/(?P<dd_id>\d+)/$', 'detail', name='detail'),
    url('^add/', 'add', name='add'),
)