import pytest
from django.core.urlresolvers import reverse
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_list_proposals_pass(client, settings):
    conference = f.create_conference()
    url = reverse('proposals-list', kwargs={'conference_slug': conference.slug})
    response = client.get(url)

    assert response.status_code == 200


def test_list_proposals_fail(client, settings):
    url = reverse('proposals-list', kwargs={'conference_slug': 'conf-404'})
    response = client.get(url)

    assert response.status_code == 404
