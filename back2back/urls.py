from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views


urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^entries/(?P<category>[a-z-]+)/$', views.EntryList.as_view(), name='entry-list'),
    url(r'^entries/(?P<category>[a-z-]+)/add/$', views.EntryAdd.as_view(), name='entry-add'),
    url(r'^entries/(?P<category>[a-z-]+)/edit/(?P<entry>\d+)/$', views.EntryEdit.as_view(), name='entry-edit'),
    url(r'^admin/', include(admin.site.urls)),
)
