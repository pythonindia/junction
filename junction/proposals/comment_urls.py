from django.conf.urls import patterns, url

from .views import create_proposal_comment


urlpatterns = patterns(
    '',
    url(r'^(?P<proposal_slug>[\w-]+)/create/$', create_proposal_comment, name='proposal-comment-create'),
)
