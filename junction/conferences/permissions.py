# -*- coding: utf-8 -*-

from .models import ConferenceProposalReviewer


def is_reviewer(user, conference):
    if not user.is_authenticated():
        return False

    reviewer = ConferenceProposalReviewer.objects.filter(
        reviewer=user, conference=conference,
        active=True).exists()
    return reviewer
