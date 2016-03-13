# -*- coding: utf-8 -*-


from .models import ConferenceModerator


def list_conference_moderator(user):
    qs = ConferenceModerator.objects.filter(moderator=user)
    return qs.all()
