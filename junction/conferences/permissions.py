# -*- coding: utf-8 -*-

from .models import ConferenceProposalReviewer


def is_reviewer(user, conference):
    """Returns a boolean indicating if a given user is a conference reviewer.
    """
    if not user.is_authenticated:
        return False

    qs = ConferenceProposalReviewer.objects.filter(
        reviewer=user, conference=conference, active=True
    )
    return qs.exists()
