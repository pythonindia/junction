# -*- coding: utf-8 -*-

import pytest
from django.core.urlresolvers import reverse
from rest_framework import status


pytestmark = pytest.mark.django_db


class TestProposalListApi:

    def test_get_proposals_list_without_conference(self, client):
        url = '{}?conference={}'.format(reverse('proposals-list-api'), 'foo')
        res = client.get(url)

        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 0

    def test_get_proposals_list(self, client, conferences, create_proposals):
        conference = conferences['future']
        url = '{}?conference={}'.format(reverse('proposals-list-api'), conference.slug)
        res = client.get(url)

        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 30
        assert res.data['next'] == 'http://testserver/api/v1/proposals/?conference=future&page=2'
        assert res.data['results'] != []
