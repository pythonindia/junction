import pytest
from django.core.urlresolvers import reverse
from .. import factories as f

pytestmark = pytest.mark.django_db


def test_list_proposals(client, settings):
    conference = f.create_conference()
    # proposal = f.create_proposal()

    url = reverse('proposals-list', kwargs={'conference_slug': conference.slug})
    r = client.get(url)

    assert r.status_code == 200
