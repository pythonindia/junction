# Third Party Stuff
from django.conf.urls import patterns, url

from .views import proposal_vote_down, proposal_vote_up

urlpatterns = patterns(
    '',
    url(r'^(?P<proposal_slug>[\w-]+)/up-vote/$',
        proposal_vote_up, name='proposal-vote-up'),
    url(r'^(?P<proposal_slug>[\w-]+)/down-vote/$',
        proposal_vote_down, name='proposal-vote-down'),
)
