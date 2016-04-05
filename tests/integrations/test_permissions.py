# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse

pytestmark = pytest.mark.django_db


def test_public_urls(client):

    public_urls = [
        reverse('page-home'),
        '/nimda/login/',
    ]

    for url in public_urls:
        response = client.get(url)
        assert response.status_code == 200
