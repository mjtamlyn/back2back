from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', views.PublicIndex.as_view(), name='public-index'),
    url(r'^scorers/$', views.ScorersIndex.as_view(), name='index'),
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
    url(r'^(?P<category>[a-z-]+)/first-round/scoresheets/$', views.FirstRoundScoresheets.as_view(), name='first-round-scoresheets'),
    url(r'^(?P<category>[a-z-]+)/first-round/judges/$', views.FirstRoundJudges.as_view(), name='first-round-judges'),
    url(r'^first-round/leaderboard/recurve/$', views.FirstRoundLeaderboardExportRecurve.as_view(), name='first-round-leaderboard-export-recurve'),
    url(r'^first-round/leaderboard/compound/$', views.FirstRoundLeaderboardExportCompound.as_view(), name='first-round-leaderboard-export-compound'),

    url(r'^(?P<category>[a-z-]+)/first-round/$', views.PublicFirstRound.as_view(), name='public-first-round'),

    url(r'^(?P<category>[a-z-]+)/second-round/set-groups/$', views.SecondRoundSetGroups.as_view(), name='second-round-set-groups'),
    url(r'^(?P<category>[a-z-]+)/second-round/matches/$', views.SecondRoundMatches.as_view(), name='second-round-matches'),
    url(r'^(?P<category>[a-z-]+)/second-round/matches/(?P<group>\d+)/(?P<time>\d+)/(?P<match>\d+)/$', views.SecondRoundMatchRecord.as_view(), name='second-round-match-record'),
    url(r'^(?P<category>[a-z-]+)/second-round/leaderboard/$', views.SecondRoundLeaderboard.as_view(), name='second-round-leaderboard'),
    url(r'^(?P<category>[a-z-]+)/second-round/scoresheets/$', views.SecondRoundScoresheets.as_view(), name='second-round-scoresheets'),
    url(r'^(?P<category>[a-z-]+)/second-round/judges/$', views.SecondRoundJudges.as_view(), name='second-round-judges'),
    url(r'^second-round/leaderboard/$', views.SecondRoundLeaderboardExport.as_view(), name='second-round-leaderboard-export'),

    url(r'^(?P<category>[a-z-]+)/second-round/$', views.PublicSecondRound.as_view(), name='public-second-round'),

    url(r'^(?P<category>[a-z-]+)/third-round/set-groups/$', views.ThirdRoundSetGroups.as_view(), name='third-round-set-groups'),
    url(r'^(?P<category>[a-z-]+)/third-round/matches/$', views.ThirdRoundMatches.as_view(), name='third-round-matches'),
    url(r'^(?P<category>[a-z-]+)/third-round/matches/(?P<group>\d+)/(?P<time>\d+)/(?P<match>\d+)/$', views.ThirdRoundMatchRecord.as_view(), name='third-round-match-record'),
    url(r'^(?P<category>[a-z-]+)/third-round/leaderboard/$', views.ThirdRoundLeaderboard.as_view(), name='third-round-leaderboard'),
    url(r'^(?P<category>[a-z-]+)/third-round/scoresheets/$', views.ThirdRoundScoresheets.as_view(), name='third-round-scoresheets'),
    url(r'^(?P<category>[a-z-]+)/third-round/judges/$', views.ThirdRoundJudges.as_view(), name='third-round-judges'),
    url(r'^third-round/leaderboard/$', views.ThirdRoundLeaderboardExport.as_view(), name='third-round-leaderboard-export'),

    url(r'^(?P<category>[a-z-]+)/third-round/$', views.PublicThirdRound.as_view(), name='public-third-round'),

    url(r'^(?P<category>[a-z-]+)/finals/set-seeds/$', views.FinalsSetSeeds.as_view(), name='finals-set-seeds'),
    url(r'^finals/$', views.Finals.as_view(), name='finals'),
    url(r'^finals/(?P<category>[a-z-]+)/(?P<match>\d+)/$', views.FinalsMatchRecord.as_view(), name='finals-match-record'),
    url(r'^finals/scoresheets/$', views.FinalsScoresheets.as_view(), name='finals-scoresheets'),

    url(r'^(?P<category>[a-z-]+)/finals/$', views.PublicFinals.as_view(), name='public-finals'),

    url(r'^results/$', views.ResultsPDF.as_view(), name='results-pdf'),

    url(r'^admin/', include(admin.site.urls)),
)
