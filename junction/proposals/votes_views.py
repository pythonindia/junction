# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponse, HttpResponseRedirect

from junction.base.constants import ProposalUserVoteRole
from junction.conferences.models import Conference

from .forms import ProposalReviewerVoteForm

from .models import (
    Proposal,
    ProposalVote,
    ProposalComment,
    ProposalCommentVote,
    ProposalSectionReviewerVote,
    ProposalSectionReviewer,
    ProposalSectionReviewerVoteValue)

from . import permissions


@login_required
def proposal_vote(request, conference_slug, proposal_slug, up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(
        Proposal, slug=proposal_slug, conference=conference)

    proposal_vote, created = ProposalVote.objects.get_or_create(
        proposal=proposal, voter=request.user)  # @UnusedVariable

    if permissions.is_proposal_reviewer(request.user, conference):
        role = ProposalUserVoteRole.REVIEWER
    else:
        role = ProposalUserVoteRole.PUBLIC

    proposal_vote.role = role
    proposal_vote.up_vote = up_vote
    proposal_vote.save()

    return HttpResponse(proposal.get_votes_count())


@login_required
@require_http_methods(['POST'])
def proposal_vote_up(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, True)


@login_required
@require_http_methods(['POST'])
def proposal_vote_down(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, False)


def proposal_comment_vote(request, conference_slug, proposal_slug, comment_id,
                          up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug,
                                 conference=conference)
    proposal_comment = get_object_or_404(ProposalComment, proposal=proposal,
                                         id=comment_id)
    proposal_comment_vote, created = ProposalCommentVote.objects.get_or_create(
        proposal_comment=proposal_comment, voter=request.user)
    proposal_comment_vote.up_vote = up_vote
    proposal_comment_vote.save()

    return HttpResponseRedirect(reverse('proposal-detail',
                                        args=[conference.slug, proposal.slug]))


@login_required
@require_http_methods(['POST'])
def proposal_comment_up_vote(request, conference_slug, proposal_slug,
                             proposal_comment_id):
    return proposal_comment_vote(request, conference_slug, proposal_slug,
                                 proposal_comment_id, True)


@login_required
@require_http_methods(['POST'])
def proposal_comment_down_vote(request, conference_slug, proposal_slug,
                               proposal_comment_id):
    return proposal_comment_vote(request, conference_slug, proposal_slug,
                                 proposal_comment_id, False)


@login_required
@require_http_methods(['GET', 'POST'])
def proposal_reviewer_vote(request, conference_slug, proposal_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug,
                                 conference=conference)

    if not permissions.is_proposal_section_reviewer(request.user,
                                                    conference, proposal):
        raise PermissionDenied

    vote_value = None

    try:
        vote = ProposalSectionReviewerVote.objects.get(
            proposal=proposal,
            voter=ProposalSectionReviewer.objects.get(
                conference_reviewer__reviewer=request.user,
                conference_reviewer__conference=conference,
                proposal_section=proposal.proposal_section),
        )
        vote_value = vote.vote_value.vote_value
    except ProposalSectionReviewerVote.DoesNotExist:
        vote = None

    try:
        vote_comment = ProposalComment.objects.get(
            proposal=proposal,
            commenter=request.user,
            vote=True,
            deleted=False,
        )
    except:
        vote_comment = None
    if request.method == 'GET':
        if vote_comment:
            proposal_vote_form = ProposalReviewerVoteForm(
                initial={'vote_value': vote_value,
                         'comment': vote_comment.comment})
        else:
            proposal_vote_form = ProposalReviewerVoteForm(
                initial={'vote_value': vote_value})
        ctx = {
            'proposal': proposal,
            'proposal_vote_form': proposal_vote_form,
            'vote': vote,
        }

        return render(request, 'proposals/vote.html', ctx)

    # POST Workflow
    form = ProposalReviewerVoteForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'proposals/vote.html',
                      {'form': form,
                       'proposal': proposal,
                       'form_errors': form.errors})

    # Valid Form
    vote_value = form.cleaned_data['vote_value']
    comment = form.cleaned_data['comment']
    if not vote:
        vote = ProposalSectionReviewerVote.objects.create(
            proposal=proposal,
            voter=ProposalSectionReviewer.objects.filter(
                conference_reviewer__reviewer=request.user,
                conference_reviewer__conference=conference,
                proposal_section=proposal.proposal_section)[0],
            vote_value=ProposalSectionReviewerVoteValue.objects.filter(
                vote_value=vote_value)[0],
        )
    else:
        vote.vote_value = ProposalSectionReviewerVoteValue.objects.filter(
            vote_value=vote_value)[0]
        vote.save()
    if not vote_comment:
        vote_comment = ProposalComment.objects.create(
            proposal=proposal,
            commenter=request.user,
            comment=comment,
            vote=True,
        )
    else:
        vote_comment.comment = comment
        vote_comment.save()
    return HttpResponseRedirect(reverse('proposals-to-review',
                                        args=[conference.slug]))
