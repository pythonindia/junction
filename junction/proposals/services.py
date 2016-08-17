# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections
import logging

from markdown2 import markdown
from django.conf import settings
from django.core.exceptions import PermissionDenied

from junction.base.constants import PSRVotePhase, ProposalCommentType, \
    ProposalReviewVote, ProposalStatus, ProposalVotesFilter
from junction.base.emailer import send_email
from junction.proposals.models import ProposalComment, \
    ProposalSectionReviewerVote, ProposalSectionReviewerVoteValue
from . import permissions
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


def send_mail_for_proposal_content(conference, proposal, host):
    """
    Send mail to proposal author to upload content for proposal.
    """
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


def _arrange_proposals_by_section(proposal_qs):
    res = collections.defaultdict(list)
    for proposal in proposal_qs:
        res[proposal.proposal_section.name].append(proposal)
    return res


def get_reviewer_vote_info(user, conference, proposal, vote_phase):

    if vote_phase == PSRVotePhase.PRIMARY:
        comment_type = ProposalCommentType.GENERAL
    elif vote_phase == PSRVotePhase.SECONDARY:
        comment_type = ProposalCommentType.SECONDARY_VOTING

    if not (permissions.is_proposal_section_reviewer(user,
                                                     conference, proposal) and
            permissions.is_proposal_voting_allowed(proposal)):
        raise PermissionDenied

    voter = ProposalSectionReviewer.objects.get(
        conference_reviewer__reviewer=user,
        conference_reviewer__conference=conference,
        proposal_section=proposal.proposal_section)

    try:
        psr_vote = ProposalSectionReviewerVote.objects.get(proposal=proposal, voter=voter, phase=vote_phase)
    except ProposalSectionReviewerVote.DoesNotExist:
        psr_vote = None

    try:
        vote_comment = ProposalComment.objects.get(
            proposal=proposal,
            commenter=user,
            vote=True,
            deleted=False,
            comment_type=comment_type,
        )
    except:
        vote_comment = None

    return psr_vote, vote_comment


def update_reviewer_vote_info(user, psr_vote, vote_value, comment, phase, proposal, conference):

    if phase == PSRVotePhase.PRIMARY:
        comment_type = ProposalCommentType.GENERAL
    elif phase == PSRVotePhase.SECONDARY:
        comment_type = ProposalCommentType.SECONDARY_VOTING

    voter = ProposalSectionReviewer.objects.filter(
        conference_reviewer__reviewer=user,
        conference_reviewer__conference=conference,
        proposal_section=proposal.proposal_section)[0]

    vote_value = ProposalSectionReviewerVoteValue.objects.filter(vote_value=vote_value)[0]

    psr_vote, _ = ProposalSectionReviewerVote.objects.update_or_create(
        proposal=proposal, voter=voter, phase=phase,
        defaults={'vote_value': vote_value}
    )

    p_comment, _ = ProposalComment.objects.update_or_create(
        proposal=proposal, commenter=user, vote=True, comment_type=comment_type,
        defaults={'comment': comment}
    )

    return psr_vote, p_comment


def _sort_proposals_for_dashboard(conference, proposals_qs, user, form):
    cps = form.cleaned_data['proposal_section']
    cpt = form.cleaned_data['proposal_type']
    votes = form.cleaned_data['votes']
    review_status = form.cleaned_data['review_status']

    proposal_sections = conference.proposal_sections.all()
    s_items = collections.namedtuple('section_items', 'section proposals')
    proposals = []

    if cps != 'all':
        proposal_sections = ProposalSection.objects.filter(pk=cps)
    if cpt != 'all':
        proposals_qs = proposals_qs.filter(proposal_type__id__in=cpt)
    if votes != 'all':
        votes = int(votes)
    if review_status != 'all':
        proposals_qs = proposals_qs.filter(review_status=review_status)

    if votes == ProposalVotesFilter.NO_VOTES:
        proposals_qs = [
            p for p in proposals_qs if p.get_reviewer_votes_count() == votes]
    elif votes == ProposalVotesFilter.MIN_ONE_VOTE:
        proposals_qs = [
            p for p in proposals_qs if p.get_reviewer_votes_count() >= votes]
    elif votes == ProposalVotesFilter.SORT_BY_REVIEWER:
        proposals_qs = sorted(
            proposals_qs,
            key=lambda x: x.get_reviewer_vote_value(reviewer=user),
            reverse=True,
        )
    elif votes == ProposalVotesFilter.SORT_BY_SUM:
        proposals_qs = sorted(
            proposals_qs, key=lambda x: x.get_reviewer_votes_sum(),
            reverse=True)
        proposals = [s_items('', proposals_qs)]

    elif votes == ProposalVotesFilter.SORT_BY_SELECTION:
        # Selection of proposal is based on conference guidelines.
        # More info is available at http://tiny.cc/qzo5cy

        proposals_qs = [p for p in proposals_qs if not p.has_negative_votes()]
        proposals_qs = sorted(proposals_qs, key=lambda x: x.get_reviewer_votes_sum(), reverse=True)

        selected = [p for p in proposals_qs if p.get_reviewer_votes_count_by_value(ProposalReviewVote.MUST_HAVE) >= 2]
        proposals.append(s_items('Selected', selected))

        batch1 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.MUST_HAVE) == 1 and
                  p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) > 2]
        proposals.append(s_items('1 Must Have & 2+ Good Votes', batch1))

        batch2 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.MUST_HAVE) == 1 and
                  p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) == 1]
        proposals.append(s_items('1 Must Have & 1 Good Vote', batch2))

        batch3 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) > 2 and
                  p not in batch1]
        proposals.append(s_items('2+ Good Votes', batch3))

        batch4 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) == 1 and
                  p.get_reviewer_votes_count_by_value(ProposalReviewVote.NOT_BAD) > 2 and
                  p not in batch2]
        proposals.append(s_items('1 Good & 2+ Not Bad votes', batch4))

    if votes not in (ProposalVotesFilter.SORT_BY_SUM, ProposalVotesFilter.SORT_BY_SELECTION):
        for section in proposal_sections:
            section_proposals = [p for p in proposals_qs if p.proposal_section == section]
            proposals.append(s_items(section, section_proposals))

    return proposals
