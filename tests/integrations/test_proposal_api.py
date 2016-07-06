# -*- coding: utf-8 -*-

import pytest
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status


pytestmark = pytest.mark.django_db


class TestProposalListApi:

    def test_get_proposals_list_without_conference(self, client):
        url = '{}?conference={}'.format(reverse('proposals-list-api'), 'foo')
        res = client.get(url)

        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 0

    def test_get_proposals_list(self, client, conferences, create_proposal):
        conference = conferences['future']
        url = '{}?conference={}'.format(reverse('proposals-list-api'), conference.slug)
        res = client.get(url)

        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 1
        assert res.data['results'] != []
