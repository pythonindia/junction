from django.conf.urls import patterns, url

from proposals.views import proposal_vote_up, proposal_vote_down


urlpatterns = patterns(
    '',
    url(r'^(?P<proposal_slug>[\w-]+)/up-vote/$',
        proposal_vote_up, name='proposal-vote-up'),
    url(r'^(?P<proposal_slug>[\w-]+)/down-vote/$',
        proposal_vote_down, name='proposal-vote-down'),
)
