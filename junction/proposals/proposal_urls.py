# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',

    url(r'^$', views.list_proposals, name='proposals-list'),
    url(r'^create/$', views.create_proposal, name='proposal-create'),
    url(r'^(?P<slug>[\w-]+)/update$',
        views.update_proposal, name='proposal-update'),
    url(r'^(?P<slug>[\w-]+)/$', views.detail_proposal, name='proposal-detail'),
    url(r'^(?P<slug>[\w-]+)/delete/$',
        views.delete_proposal, name='proposal-delete'),

    # Voting
    url(r'^(?P<proposal_slug>[\w-]+)/up-vote/$',
        views.proposal_vote_up, name='proposal-vote-up'),
    url(r'^(?P<proposal_slug>[\w-]+)/down-vote/$',
        views.proposal_vote_down, name='proposal-vote-down'),
)
