from django import template
register = template.Library()
from junction.proposals import models


@register.assignment_tag
def get_comment_vote_value(comment_id, user):

    comment_note_value = 0
    vote = models.ProposalCommentVote.objects.filter(proposal_comment_id=comment_id, voter=user)
    if vote.exists():
        if vote[0].up_vote == True:
            comment_note_value = 1
        else:
            comment_note_value = -1
    return comment_note_value
