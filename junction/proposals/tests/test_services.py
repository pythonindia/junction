# -*- coding: utf-8 -*-

# Third Party Stuff
from django.test import TestCase

# Junction Stuff
from junction.proposals.services import post_tweet_for_new_proposal


class TestServices(TestCase):

    def test_post_tweet_for_new_proposal(self):
        proposal_name = 'test proposal'
        proposal_url = 'http://in.pycon.org/2015/'
        response = post_tweet_for_new_proposal(proposal_name, proposal_url)
        self.assertEqual(response.status_code, 200)
