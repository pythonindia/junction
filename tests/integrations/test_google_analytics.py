import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_google_analytics_rendering(client, settings):
    url = reverse("page-home")

    response = client.get(url)
    assert b"UA-MY-ID" not in response.content

    settings.SITE_VARIABLES["google_analytics_id"] = "UA-MY-ID"
    response = client.get(url)
    assert b"UA-MY-ID" in response.content
