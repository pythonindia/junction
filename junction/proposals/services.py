# -*- coding: utf-8 -*-

# Third Party Stuff
from django.conf import settings

# Junction Stuff
from junction.base.emailer import send_email

from .models import ProposalSection, ProposalSectionReviewer


def send_mail_for_new_comment(proposal_comment, host, login_url):
    proposal = proposal_comment.proposal
    send_to = comment_recipients(proposal_comment)
    commenter = proposal_comment.commenter
    for to in send_to:
        if to == proposal_comment.commenter:
            continue
        send_email(to=to,
                   template_dir='proposals/email/comment',
                   context={'to': to,
                            'proposal': proposal,
                            'comment': proposal_comment,
                            'commenter': commenter,
                            'host': host,
                            'login_url': login_url})


def comment_recipients(proposal_comment):
    proposal = proposal_comment.proposal
    if proposal_comment.private:
        proposal_reviewers = set(ProposalSectionReviewer.objects.filter(
            proposal_section=proposal.proposal_section))
        recipients = {proposal_reviewer.conference_reviewer.reviewer
                      for proposal_reviewer in proposal_reviewers}
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
