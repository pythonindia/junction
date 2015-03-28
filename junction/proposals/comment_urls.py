# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^(?P<proposal_slug>[\w-]+)/create/$',
        views.create_proposal_comment, name='proposal-comment-create'),
    url(r'^(?P<proposal_slug>[\w-]+)/comments/(?P<proposal_comment_id>\d+)/up-vote/$',
        views.proposal_comment_up_vote, name='proposal-comment-up-vote'),
    url(r'^(?P<proposal_slug>[\w-]+)/comments/(?P<proposal_comment_id>\d+)/down-vote/$',
        views.proposal_comment_down_vote, name='proposal-comment-down-vote'),
)
