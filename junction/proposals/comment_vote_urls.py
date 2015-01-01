from django.conf.urls import patterns, url

from proposals.views import proposal_comment_vote_up, proposal_comment_vote_down


urlpatterns = patterns(
    '',
    url(r'^(?P<proposal_slug>[\w-]+)/(?P<proposal_comment_id>\d+)/up-vote/$',
        proposal_comment_vote_up, name='proposal-comment-up-vote'),
    url(r'^(?P<proposal_slug>[\w-]+)/(?P<proposal_comment_id>\d+)/down-vote/$',
        proposal_comment_vote_down, name='proposal-comment-down-vote'),
)