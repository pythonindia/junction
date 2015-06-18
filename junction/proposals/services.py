# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import logging

# Third Party Stuff
from django.conf import settings
from markdown2 import markdown


# Junction Stuff
from junction.base.emailer import send_email

from .models import ProposalSection, ProposalSectionReviewer

logger = logging.getLogger(__name__)


def markdown_to_html(md):
    """
    Convert given markdown to html.
    :param md: string
    :return: string - converted html
    """
    return markdown(md)


def send_mail_for_new_comment(proposal_comment, host):
    proposal = proposal_comment.proposal
    login_url = '{}?next={}'.format(settings.LOGIN_URL, proposal.get_absolute_url())
    send_to = comment_recipients(proposal_comment)
    commenter = proposal_comment.commenter
    proposal_comment.comment = markdown_to_html(proposal_comment.comment)
    for to in send_to:
        if to == proposal_comment.commenter:
            continue
        send_email(to=to,
                   template_dir='proposals/email/comment',
                   context={'to': to,
                            'host': host,
                            'login_url': login_url,
                            'proposal': proposal,
                            'comment': proposal_comment,
                            'commenter': commenter,
                            'by_author': commenter == proposal.author})


def comment_recipients(proposal_comment):
    proposal = proposal_comment.proposal
    if proposal_comment.private:
        recipients = _get_proposal_section_reviewers(
            proposal=proposal)
    else:
        recipients = {
            comment.commenter
            for comment in proposal.proposalcomment_set
            .all().select_related('commenter')}
    if proposal_comment.reviewer:
        # Don't add proposer to reviwer only comments
        section_reviewers = _get_proposal_section_reviewers(
            proposal=proposal)
        recipients.union(section_reviewers)
    else:
        recipients.add(proposal.author)

    return recipients


def send_mail_for_new_proposal(proposal, host):
    proposal_section = ProposalSection.objects.get(
        pk=proposal.proposal_section_id)
    send_to = [p.conference_reviewer.reviewer for p in
               ProposalSectionReviewer.objects.filter(
                   proposal_section=proposal_section,
                   active=True)]
    proposal_url = proposal.get_absolute_url()
    login_url = settings.LOGIN_URL
    for to in send_to:
        if to == proposal.author:
            continue
        send_email(to=to,
                   template_dir='proposals/email/proposal',
                   context={'to': to,
                            'proposal': proposal,
                            'proposal_section': proposal_section,
                            'host': host,
                            'proposal_url': proposal_url,
                            'login_url': login_url})


def _get_proposal_section_reviewers(proposal):
    proposal_reviewers = set(ProposalSectionReviewer.objects.filter(
        proposal_section=proposal.proposal_section))
    recipients = {proposal_reviewer.conference_reviewer.reviewer
                  for proposal_reviewer in proposal_reviewers}
    return recipients
