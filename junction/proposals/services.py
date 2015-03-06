# -*- coding: utf-8 -*-

import logging

# Third Party Stuff
from django.conf import settings
from TwitterAPI import TwitterAPI

# Junction Stuff
from junction.base.emailer import send_email

from .models import ProposalSection, ProposalSectionReviewer


logger = logging.getLogger(__name__)


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


def post_tweet_for_new_proposal(proposal_name, proposal_url):
    """
    Post a tweet from junction twitter handler when a proposal is created.
    """
    try:
        twitter_api = TwitterAPI(settings.TWITTER_CONSUMER_KEY,
                                 settings.TWITTER_CONSUMER_SECRET,
                                 settings.TWITTER_ACCESS_TOKEN_KEY,
                                 settings.TWITTER_ACCESS_TOKEN_SECRET)
        tweet_text = "New proposal: {0}".format(proposal_name)

        # twitter uses 26 chars for links, so text is limited to 114 chars.
        if len(tweet_text) > 114:
            tweet_text = "{0}...".format(tweet_text[:110])
        tweet = "{0} {1}".format(tweet_text, proposal_url)
        response = twitter_api.request('statuses/update', {'status': tweet})
        return response
    except:
        logger.error('Unable to post tweet for {0} {1}'.
                     format(proposal_name, proposal_url))
