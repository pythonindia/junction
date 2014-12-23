from django.conf.urls import patterns, url

from proposals.views import create_proposal, list_proposals, update_proposal, detail_proposal, delete_proposal


urlpatterns = patterns('',
    url(r'^$', list_proposals, name='proposals-list'),
    url(r'^create/$', create_proposal, name='proposal-create'),
    url(r'^update/(?P<slug>[\w-]+)/$', update_proposal, name='proposal-update'),
    url(r'^(?P<slug>[\w-]+)/$', detail_proposal, name='proposal-detail'),
    url(r'^delete/(?P<proposal_id>\d+)/$', delete_proposal, name='proposal-delete'),
)
