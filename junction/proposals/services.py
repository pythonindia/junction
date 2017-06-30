# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

# Standard Library
import logging
import collections

# Third Party Stuff
from django.conf import settings
from django.contrib.auth.models import User
from markdown2 import markdown
from celery import shared_task

# Junction Stuff
from junction.base.emailer import send_email
from junction.base.constants import ProposalStatus

from .models import Proposal, ProposalComment, ProposalSection, ProposalSectionReviewer
from junction.conferences.models import Conference

logger = logging.getLogger(__name__)


def _get_proposal_section_reviewers(proposal):
    proposal_reviewers = set(ProposalSectionReviewer.objects.filter(
        proposal_section=proposal.proposal_section))
    recipients = {proposal_reviewer.conference_reviewer.reviewer
                  for proposal_reviewer in proposal_reviewers}
    return recipients


def _arrange_proposals_by_section(proposal_qs):
    res = collections.defaultdict(list)
    for proposal in proposal_qs:
        res[proposal.proposal_section.name].append(proposal)
    return res


def group_proposals_by_reveiew_state(conf, state='reviewed'):
    reviewed_qs = conf.proposal_set.filter(
        status=ProposalStatus.PUBLIC).select_related(
            'proposal_type', 'proposal_section',
            'proposalsection').filter(proposalcomment__private=True,
                                      proposalcomment__deleted=False)
    if state == 'reviewed':
        proposal_qs = reviewed_qs.distinct()
        return _arrange_proposals_by_section(proposal_qs)
    else:
        ids = reviewed_qs.values_list('id').distinct()
        qs = conf.proposal_set.filter(
            status=ProposalStatus.PUBLIC).select_related(
                'proposal_type', 'proposal_section',
                'proposalsection').exclude(pk__in=ids)
        return _arrange_proposals_by_section(qs)


def markdown_to_html(md):
    """
    Convert given markdown to html.
    :param md: string
    :return: string - converted html
    """
    return markdown(md)


def comment_recipients(proposal_comment):
    proposal = proposal_comment.proposal
    if proposal_comment.reviewer:
        recipients = _get_proposal_section_reviewers(
            proposal=proposal)
    elif proposal_comment.private:
        recipients = _get_proposal_section_reviewers(
            proposal=proposal)
        recipients.add(proposal.author)
    else:
        recipients = {
            comment.commenter
            for comment in proposal.proposalcomment_set
            .all().select_related('commenter')}
        recipients.add(proposal.author)
        ADMINS = getattr(settings, 'SPAM_MODERATION_ADMINS', [])
        if ADMINS:
            for admin in ADMINS:
                recipients.add(User.objects.get(email=admin))

    return recipients


@shared_task(ignore_result=True)
def send_mail_for_new_comment(proposal_comment_id, host):
    proposal_comment = ProposalComment.objects.get(id=proposal_comment_id)
    proposal = proposal_comment.proposal
    login_url = '{}?next={}'.format(settings.LOGIN_URL, proposal.get_absolute_url())
    send_to = comment_recipients(proposal_comment)
    commenter = proposal_comment.commenter
    comment_type = proposal_comment.get_comment_type()
    comment_html = markdown_to_html(proposal_comment.comment)
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
                            'comment_html': comment_html,
                            'commenter': commenter,
                            'by_author': commenter == proposal.author,
                            'comment_type': comment_type})


@shared_task(ignore_result=True)
def send_mail_for_new_proposal(proposal_id, host):
    proposal = Proposal.objects.get(id=proposal_id)
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


@shared_task(ignore_result=True)
def send_mail_for_proposal_content(conference_id, proposal_id, host):
    """
    Send mail to proposal author to upload content for proposal.
    """
    conference = Conference.objects.get(id=conference_id)
    proposal = Proposal.objects.get(id=proposal_id)
    login_url = '{}?next={}'.format(settings.LOGIN_URL, proposal.get_absolute_url())
    author = proposal.author
    author_name = author.get_full_name() or author.username
    context = {
        'host': host,
        'login_url': login_url,
        'conference': conference,
        'proposal': proposal,
        'author_name': author_name,
    }
    return send_email(to=author, template_dir='proposals/email/upload_content',
                      context=context)


def user_action_for_spam(user, threshold):
    """When a comment is marked as spam, make appropriate status update to user model
    """
    total_spam = ProposalComment.objects.filter(commenter=user, is_spam=True).count()
    if total_spam >= threshold:
        if user.is_active is True:
            user.is_active = False
            user.save()
    else:
        if user.is_active is False:
            user.is_active = True
            user.save()
