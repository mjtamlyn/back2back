from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views


urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^(?P<category>[a-z-]+)/entries/$', views.EntryList.as_view(), name='entry-list'),
    url(r'^(?P<category>[a-z-]+)/entries/add/$', views.EntryAdd.as_view(), name='entry-add'),
    url(r'^(?P<category>[a-z-]+)/entries/edit/(?P<entry>\d+)/$', views.EntryEdit.as_view(), name='entry-edit'),
    url(r'^(?P<category>[a-z-]+)/entries/delete/(?P<entry>\d+)/$', views.EntryDelete.as_view(), name='entry-delete'),
    url(r'^(?P<category>[a-z-]+)/first-round/set-groups/$', views.FirstRoundSetGroups.as_view(), name='first-round-set-groups'),
    url(r'^(?P<category>[a-z-]+)/first-round/set-groups/add/$', views.FirstRoundGroupAdd.as_view(), name='first-round-group-add'),
    url(r'^(?P<category>[a-z-]+)/first-round/set-groups/remove/$', views.FirstRoundGroupRemove.as_view(), name='first-round-group-remove'),
    url(r'^admin/', include(admin.site.urls)),
)
