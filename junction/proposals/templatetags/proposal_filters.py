# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import re

# Third Party Stuff
from django import template

# Junction Stuff
from junction.proposals.models import (
    ProposalSectionReviewer,
    ProposalSectionReviewerVote,
)


register = template.Library()


@register.filter(name='reviewer_comments')
def reviewer_comments(proposal, user):
    return proposal.get_reviewer_comments_count(user) > 0


@register.filter(name='is_reviewer_voted')
def is_reviewer_voted(proposal, user):
    try:
        vote = ProposalSectionReviewerVote.objects.get(
            proposal=proposal,
            voter=ProposalSectionReviewer.objects.get(
                conference_reviewer__reviewer=user,
                conference_reviewer__conference=proposal.conference,
                proposal_section=proposal.proposal_section),
        )
    except ProposalSectionReviewerVote.DoesNotExist:
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
