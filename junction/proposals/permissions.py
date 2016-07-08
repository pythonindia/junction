# -*- coding: utf-8 -*-

# Third Party Stuff
from django.core.exceptions import PermissionDenied

# Junction Stuff
from junction.conferences.models import ConferenceProposalReviewer
from junction.base.constants import ConferenceStatus

from .models import ProposalSectionReviewer


def is_proposal_voting_allowed(proposal):
    return proposal.conference.status != ConferenceStatus.SCHEDULE_PUBLISHED


def is_proposal_author(user, proposal):
    return user.is_authenticated() and proposal.author == user


def is_proposal_reviewer(user, conference):
    authenticated = user.is_authenticated()
    is_reviewer = ConferenceProposalReviewer.objects.filter(
        reviewer=user.id, conference=conference, active=True).exists()
    return authenticated and is_reviewer


def is_proposal_section_reviewer(user, conference, proposal):
    return user.is_authenticated() and ProposalSectionReviewer.objects.filter(
        conference_reviewer__reviewer=user,
        conference_reviewer__conference=conference,
        proposal_section=proposal.proposal_section,
        active=True).exists()


def is_proposal_author_or_proposal_reviewer(user, conference, proposal):
    reviewer = is_proposal_reviewer(user, conference)
    author = is_proposal_author(user, proposal)
    return reviewer or author


def is_proposal_author_or_proposal_section_reviewer(user,
                                                    conference, proposal):
    return is_proposal_author(user, proposal) or \
        is_proposal_section_reviewer(user, conference, proposal)


def is_proposal_author_or_permisson_denied(user, proposal):
    if is_proposal_author(user, proposal):
        return True
    raise PermissionDenied
