# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections
import re

from django import template
from junction.base.constants import PSRVotePhase
from junction.proposals.models import ProposalComment, ProposalSectionReviewer, \
    ProposalSectionReviewerVote


register = template.Library()


@register.filter(name='reviewer_comments')
def reviewer_comments(proposal, user):
    return proposal.get_reviewer_comments_count(user) > 0


@register.filter(name='is_reviewer_voted')
def is_reviewer_voted(proposal, user, phase=None):
    if not phase:
        phase = PSRVotePhase.PRIMARY

    try:
        voter = ProposalSectionReviewer.objects.get(
            conference_reviewer__reviewer=user,
            conference_reviewer__conference=proposal.conference,
            proposal_section=proposal.proposal_section
        )
        vote = ProposalSectionReviewerVote.objects.get(proposal=proposal, voter=voter, phase=phase)
    except (ProposalSectionReviewer.DoesNotExist, ProposalSectionReviewerVote.DoesNotExist):
        vote = None

    return vote


@register.filter(name='get_content_urls')
def get_content_urls(proposal):
    if proposal.content_urls:
        url_re = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_re, proposal.content_urls)
        return urls
    else:
        return []


@register.filter(name='has_upvoted_comment')
def has_upvoted_comment(comment, user):
    vote = comment.proposalcommentvote_set.filter(voter=user)
    if vote:
        return vote[0].up_vote


@register.filter(name='get_reviewers_vote_details')
def get_reviewers_vote_details(proposal, user):
    """
    Get voter name & details for given proposals.
    """
    v_detail = collections.namedtuple('v_detail',
                                      'voter vote_value vote_comment')
    reviewers = ProposalSectionReviewer.objects.filter(
        proposal_section=proposal.proposal_section,
        conference_reviewer__conference=proposal.conference,
    )

    vote_details = []
    for reviewer in reviewers:
        voter = reviewer.conference_reviewer.reviewer.get_full_name()
        rv_qs = ProposalSectionReviewerVote.objects.filter(
            proposal=proposal,
            voter=reviewer)
        if rv_qs:
            vote_value = rv_qs[0].vote_value
        else:
            vote_value = None

        vc_qs = ProposalComment.objects.filter(
            proposal=proposal,
            commenter=reviewer.conference_reviewer.reviewer,
            vote=True)
        if vc_qs:
            vote_comment = vc_qs[0].comment
        else:
            vote_comment = None

        vote_details.append(v_detail(voter, vote_value, vote_comment))

    return vote_details
