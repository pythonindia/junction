# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    create_proposal,
    delete_proposal,
    detail_proposal,
    list_proposals,
    update_proposal
)

urlpatterns = patterns(
    '',

    url(r'^$', list_proposals, name='proposals-list'),
    url(r'^create/$', create_proposal, name='proposal-create'),
    url(r'^update/(?P<slug>[\w-]+)/$', update_proposal, name='proposal-update'),
    url(r'^(?P<slug>[\w-]+)/$', detail_proposal, name='proposal-detail'),
    url(r'^(?P<slug>[\w-]+)/(?P<reviewers>reviewers)/$', detail_proposal,
        name='proposal-detail-reviewers'),
    url(r'^delete/(?P<slug>[\w-]+)/$', delete_proposal, name='proposal-delete'),

)
