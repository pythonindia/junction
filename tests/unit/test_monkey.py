from django.urls import reverse


def test_patched_url_reverse(settings):
    settings.SITE_URL = ""
    url = reverse("page-home")
    assert url == "/"

    settings.SITE_URL = "https://mysite.com/junction"

    url = reverse("page-home")
    assert url == "https://mysite.com/junction/"

    settings.SITE_URL = "/junction"
    url = reverse("page-home")
    assert url == "/junction/"
