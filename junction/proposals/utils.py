from django.core.exceptions import PermissionDenied

from junction.base.constants import PSRVotePhase, ProposalCommentType
from junction.proposals import permissions
from junction.proposals.models import ProposalComment, ProposalSectionReviewer, \
    ProposalSectionReviewerVote, ProposalSectionReviewerVoteValue


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
