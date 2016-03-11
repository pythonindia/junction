# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django import template

# Junction Stuff
from junction.conferences.models import ConferenceModerator


register = template.Library()


@register.filter(name='is_conference_admin')
def is_conference_admin(user):
    authenticated = user.is_authenticated()
    is_moderator = ConferenceModerator.objects.filter(moderator=user.id, active=True).exists()
    return authenticated and is_moderator
