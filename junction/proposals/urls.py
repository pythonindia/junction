# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.conf.urls import include, url

from . import comments_views, views, votes_views, dashboard

comment_urls = [

    url(r'^(?P<proposal_slug>[\w-]+)/create/$',
        comments_views.create_proposal_comment, name='proposal-comment-create'),
    url(r'^(?P<proposal_slug>[\w-]+)/comments/(?P<proposal_comment_id>\d+)/up-vote/$',
        votes_views.proposal_comment_up_vote, name='proposal-comment-up-vote'),
    url(r'^(?P<proposal_slug>[\w-]+)/comments/(?P<proposal_comment_id>\d+)/down-vote/$',
        votes_views.proposal_comment_down_vote, name='proposal-comment-down-vote'),
    url(r'^(?P<proposal_slug>[\w-]+)/comments/(?P<proposal_comment_id>\d+)/mark_spam/$',
        comments_views.mark_comment_as_spam, name='comment_mark_spam'),
    url(r'^(?P<proposal_slug>[\w-]+)/comments/(?P<proposal_comment_id>\d+)/unmark_spam/$',
        comments_views.unmark_comment_as_spam, name='comment_unmark_spam'),
]

urlpatterns = [

    # proposal urls
    url(r'^$', views.list_proposals, name='proposals-list'),
    url(r'^create/$', views.create_proposal, name='proposal-create'),
    url(r'^to_review/$', views.proposals_to_review, name='proposals-to-review'),
    url(r'^second_phase_voting/$', dashboard.second_phase_voting, name='second-phase-voting'),
    url(r'^(?P<slug>[\w-]+)/$', views.detail_proposal, name='proposal-detail'),
    url(r'^(?P<slug>[\w-]+)~(?P<hashid>.*)/$', views.detail_proposal, name='proposal-detail'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.delete_proposal, name='proposal-delete'),
    url(r'^(?P<slug>[\w-]+)/update/$', views.update_proposal, name='proposal-update'),
    url(r'^(?P<slug>[\w-]+)/upload-content/$', views.proposal_upload_content, name='proposal-upload-content'),
    url(r'^(?P<slug>[\w-]+)/change-proposal-review-state/$', views.review_proposal, name='proposal-review'),

    # comment urls
    url(r'^comment/', include(comment_urls)),

    # Voting
    url(r'^(?P<proposal_slug>[\w-]+)/down-vote/$', votes_views.proposal_vote_down, name='proposal-vote-down'),
    url(r'^(?P<proposal_slug>[\w-]+)/up-vote/$', votes_views.proposal_vote_up, name='proposal-vote-up'),
    url(r'^(?P<proposal_slug>[\w-]+)/remove-vote/$', votes_views.proposal_vote_remove, name='proposal-vote-remove'),
    url(r'^(?P<proposal_slug>[\w-]+)/vote/$', votes_views.proposal_reviewer_vote, name='proposal-reviewer-vote'),
    url(r'^(?P<proposal_slug>[\w-]+)/second-vote/$', votes_views.proposal_reviewer_secondary_vote,
        name='proposal-reviewer-secondary-vote')
]
