# -*- coding: utf-8 -*-


def patch_urltag():
    from django.template.defaulttags import URLNode  # noqa
    from django.conf import settings  # noqa

    if hasattr(URLNode, "_patched"):
        return

    old_render = URLNode.render

    def is_absolute_url(path):
        """Test wether or not `path` is absolute url."""
        return path.startswith("http")

    def new_render(cls, context):
        path = old_render(cls, context)
        if is_absolute_url(path):
            return path

        return settings.SITE_URL + path

    URLNode._patched = True
    URLNode.render = new_render
