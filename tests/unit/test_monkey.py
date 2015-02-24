from django.core.urlresolvers import reverse


def test_patched_url_reverse(settings):
    settings.SITE_URL = ''
    url = reverse("pages:homepage")
    assert url == '/'

    settings.SITE_URL = 'https://mysite.com/junction'

    url = reverse("pages:homepage")
    assert url == 'https://mysite.com/junction/'

    settings.SITE_URL = '/junction'
    url = reverse("pages:homepage")
    assert url == '/junction/'
