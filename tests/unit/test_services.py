# -*- coding: utf-8 -*-

import os
import pytest

from django.conf import settings

from junction.proposals.services import post_tweet_for_new_proposal


@pytest.mark.skipif(os.environ.get('TRAVIS', None) == 'true',
                    reason="travis doesn't support external network connection")
def test_post_tweet_for_new_proposal():
    if all((settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_ACCESS_TOKEN_KEY,
            settings.TWITTER_ACCESS_TOKEN_SECRET)):
        proposal_name = ('test proposal too long. greater than 140 chars long.'
                         'this is too lengthy. twitter throws exception')
        proposal_url = 'http://in.pycon.org/2015/test_post_tweet_for_new_proposal/test/user'
        response = post_tweet_for_new_proposal(proposal_name, proposal_url)
        assert response.status_code == 200
