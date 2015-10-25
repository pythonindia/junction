# Third Party Stuff
import pytest
from django.core.urlresolvers import reverse

pytestmark = pytest.mark.django_db


def test_google_analytics_rendering(client, settings):
    url = reverse('pages:homepage')

    response = client.get(url)
    assert 'UA-MY-ID' not in str(response.content)

    settings.SITE_VARIABLES['google_analytics_id'] = 'UA-MY-ID'
    response = client.get(url)
    assert 'UA-MY-ID' in str(response.content)
