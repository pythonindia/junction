from junction.emailer import send_email
from junction.conferences.models import ConferenceProposalReviewer
from .models import ProposalType


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
        conference = proposal.conference
        recipients = set(conference.reviewer_set.all())
    else:
        recipients = {
            comment.commenter
            for comment in proposal.proposalcomment_set
            .all().select_related('commenter')}
    recipients.add(proposal.author)
    return recipients


def send_mail_for_new_proposal(conference, title, author, speaker_info,
                               url, proposal_section_id, host):
    proposal_section = ProposalType.objects.get(pk=proposal_section_id)
    send_to = [c.reviewer for c in
               ConferenceProposalReviewer.objects.filter(conference=conference)]
    for to in send_to:
        if to == author:
            continue
        send_email(to=to,
                   template_dir='proposals/email/proposal',
                   context={'to': to,
                            'title': title,
                            'author': author,
                            'speaker_info': speaker_info,
                            'conference': conference,
                            'proposal_section': proposal_section,
                            'url': url,
                            'host': host, })
