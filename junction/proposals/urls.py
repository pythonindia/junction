from django.conf.urls import patterns, url

from proposals.views import create_proposal, list_proposals, edit_proposal, detail_proposal


urlpatterns = patterns('',
    url(r'^$', list_proposals, name='proposals-list'),
    url(r'^create/$', create_proposal, name='proposal-create'),
    url(r'^edit/(?P<proposal_id>\d+)/$', edit_proposal, name='proposal-edit'),  # TODO: Slug based
    url(r'^proposal/(?P<proposal_id>\d+)/$', detail_proposal, name='proposal-detail'),  # TODO: Slug based
)
