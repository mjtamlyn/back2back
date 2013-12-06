from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^(?P<category>[a-z-]+)/entries/$', views.EntryList.as_view(), name='entry-list'),
    url(r'^(?P<category>[a-z-]+)/entries/add/$', views.EntryAdd.as_view(), name='entry-add'),
    url(r'^(?P<category>[a-z-]+)/entries/edit/(?P<entry>\d+)/$', views.EntryEdit.as_view(), name='entry-edit'),
    url(r'^(?P<category>[a-z-]+)/entries/delete/(?P<entry>\d+)/$', views.EntryDelete.as_view(), name='entry-delete'),

    url(r'^(?P<category>[a-z-]+)/first-round/set-groups/$', views.FirstRoundSetGroups.as_view(), name='first-round-set-groups'),
    url(r'^(?P<category>[a-z-]+)/first-round/set-groups/add/$', views.FirstRoundGroupAdd.as_view(), name='first-round-group-add'),
    url(r'^(?P<category>[a-z-]+)/first-round/set-groups/remove/$', views.FirstRoundGroupRemove.as_view(), name='first-round-group-remove'),
    url(r'^(?P<category>[a-z-]+)/first-round/matches/$', views.FirstRoundMatches.as_view(), name='first-round-matches'),
    url(r'^(?P<category>[a-z-]+)/first-round/matches/(?P<group>\d+)/(?P<time>\d+)/(?P<match>\d+)/$', views.FirstRoundMatchRecord.as_view(), name='first-round-match-record'),
    url(r'^(?P<category>[a-z-]+)/first-round/leaderboard/$', views.FirstRoundLeaderboard.as_view(), name='first-round-leaderboard'),

    url(r'^(?P<category>[a-z-]+)/second-round/set-groups/$', views.SecondRoundSetGroups.as_view(), name='second-round-set-groups'),
    url(r'^(?P<category>[a-z-]+)/second-round/matches/$', views.SecondRoundMatches.as_view(), name='second-round-matches'),
    url(r'^(?P<category>[a-z-]+)/second-round/matches/(?P<group>\d+)/(?P<time>\d+)/(?P<match>\d+)/$', views.SecondRoundMatchRecord.as_view(), name='second-round-match-record'),
    url(r'^(?P<category>[a-z-]+)/second-round/leaderboard/$', views.SecondRoundLeaderboard.as_view(), name='second-round-leaderboard'),

    url(r'^admin/', include(admin.site.urls)),
)
