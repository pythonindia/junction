from django.conf.urls import patterns, url
from .views import proposal_comment_up_vote, proposal_comment_down_vote

urlpatterns = patterns('',
	url(r'^(?P<proposal_slug>[\w-]+)/(?P<proposal_comment_id>\d+)/up-vote/$',
		proposal_comment_up_vote, name='proposal-comment-up-vote'),
	url(r'^(?P<proposal_slug>[\w-]+)/(?P<proposal_comment_id>\d+)/down-vote/$',
		proposal_comment_down_vote, name='proposal-comment-down-vote'),
)