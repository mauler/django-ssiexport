# coding: utf-8

from django.conf.urls import patterns, url


urlpatterns = patterns(
    'test_app.views',
    url(r'^article/(?P<pk>\w+)/$', 'article', name='article'),
    url(r'^$', 'index', name='index'),
)
