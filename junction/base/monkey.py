# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


def is_absolute_url(path):
    """Test wether or not `path` is absolute url."""
    return path.startswith("http")


def patch_urltag():
    from django.template.defaulttags import URLNode  # noqa
    from django.conf import settings  # noqa

    if hasattr(URLNode, "_patched"):
        return

    old_render = URLNode.render

    def new_render(cls, context):
        path = old_render(cls, context)
        if is_absolute_url(path):
            return path

        return settings.SITE_URL + path

    URLNode._patched = True
    URLNode.render = new_render


def patch_urlresolvers():
    from django.urls import get_urlconf, get_resolver    # noqa
    from django.conf import settings  # noqa
    urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    if hasattr(resolver, "_patched"):
        return

    old_reverse = resolver.reverse

    def new_reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None):
        path = old_reverse(
            viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
        )
        if is_absolute_url(path):
            return path

        return settings.SITE_URL + path

    resolver._patched = True
    resolver.reverse = new_reverse
