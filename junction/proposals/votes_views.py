# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from junction.base.constants import ConferenceSettingConstants, ProposalUserVoteRole
from junction.conferences.models import Conference

from . import permissions, utils
from .forms import ProposalReviewerVoteForm
from .models import (
    Proposal,
    ProposalComment,
    ProposalCommentVote,
    ProposalVote,
    PSRVotePhase,
)


@login_required
def proposal_vote(request, conference_slug, proposal_slug, up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)

    public_voting = ConferenceSettingConstants.ALLOW_PUBLIC_VOTING_ON_PROPOSALS
    public_voting_setting = conference.conferencesetting_set.filter(
        name=public_voting["name"]
    ).first()
    if public_voting_setting and not public_voting_setting.value:
        return HttpResponseForbidden()

    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)

    if not permissions.is_proposal_voting_allowed(proposal):
        return HttpResponseForbidden()

    if up_vote is None:
        # Remove any vote casted and return
        ProposalVote.objects.filter(proposal=proposal, voter=request.user).delete()
        return HttpResponse(proposal.get_votes_count())

    proposal_vote, created = ProposalVote.objects.get_or_create(
        proposal=proposal, voter=request.user
    )  # @UnusedVariable

    if permissions.is_proposal_reviewer(request.user, conference):
        role = ProposalUserVoteRole.REVIEWER
    else:
        role = ProposalUserVoteRole.PUBLIC

    proposal_vote.role = role
    proposal_vote.up_vote = up_vote
    proposal_vote.save()

    return HttpResponse(proposal.get_votes_count())


@login_required
@require_http_methods(["POST"])
def proposal_vote_up(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, True)


@login_required
@require_http_methods(["POST"])
def proposal_vote_down(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, False)


@login_required
@require_http_methods(["POST"])
def proposal_vote_remove(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, None)


def proposal_comment_vote(request, conference_slug, proposal_slug, comment_id, up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)
    proposal_comment = get_object_or_404(
        ProposalComment, proposal=proposal, id=comment_id
    )
    proposal_comment_vote, created = ProposalCommentVote.objects.get_or_create(
        proposal_comment=proposal_comment, voter=request.user
    )
    proposal_comment_vote.up_vote = up_vote
    proposal_comment_vote.save()

    return HttpResponse(proposal_comment.get_votes_count())


@login_required
@require_http_methods(["POST"])
def proposal_comment_up_vote(
    request, conference_slug, proposal_slug, proposal_comment_id
):
    return proposal_comment_vote(
        request, conference_slug, proposal_slug, proposal_comment_id, True
    )


@login_required
@require_http_methods(["POST"])
def proposal_comment_down_vote(
    request, conference_slug, proposal_slug, proposal_comment_id
):
    return proposal_comment_vote(
        request, conference_slug, proposal_slug, proposal_comment_id, False
    )


@login_required
@require_http_methods(["GET", "POST"])
def proposal_reviewer_vote(request, conference_slug, proposal_slug):
    user = request.user
    vote_phase = PSRVotePhase.PRIMARY
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)

    psr_vote, p_comment = utils.get_reviewer_vote_info(
        user, conference, proposal, vote_phase
    )

    if request.method == "GET":
        if psr_vote and p_comment:
            proposal_vote_form = ProposalReviewerVoteForm(
                conference=conference,
                initial={
                    "vote_value": psr_vote.vote_value.vote_value,
                    "comment": p_comment.comment,
                },
            )
        else:
            proposal_vote_form = ProposalReviewerVoteForm(conference=conference)
        ctx = {
            "proposal": proposal,
            "form": proposal_vote_form,
            "vote": psr_vote,
        }

        return render(request, "proposals/vote.html", ctx)

    # POST Workflow
    form = ProposalReviewerVoteForm(data=request.POST, conference=conference)
    if not form.is_valid():
        ctx = {"form": form, "proposal": proposal, "form_errors": form.errors}
        return render(request, "proposals/vote.html", ctx)

    # Valid Form
    vote_value = form.cleaned_data["vote_value"]
    comment = form.cleaned_data["comment"]

    utils.update_reviewer_vote_info(
        user, psr_vote, vote_value, comment, vote_phase, proposal, conference
    )
    return HttpResponseRedirect(reverse("proposals-to-review", args=[conference.slug]))


@login_required
@require_http_methods(["GET", "POST"])
def proposal_reviewer_secondary_vote(request, conference_slug, proposal_slug):
    vote_phase = PSRVotePhase.SECONDARY
    user = request.user
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)

    psr_vote, p_comment = utils.get_reviewer_vote_info(
        user, conference, proposal, vote_phase
    )

    if request.method == "GET":
        if psr_vote and p_comment:
            proposal_vote_form = ProposalReviewerVoteForm(
                conference=conference,
                initial={
                    "vote_value": psr_vote.vote_value.vote_value,
                    "comment": p_comment.comment,
                },
            )
        else:
            proposal_vote_form = ProposalReviewerVoteForm(conference=conference)
        ctx = {
            "proposal": proposal,
            "form": proposal_vote_form,
            "vote": psr_vote,
        }

        return render(request, "proposals/vote.html", ctx)

    # POST Workflow
    form = ProposalReviewerVoteForm(data=request.POST, conference=conference)
    if not form.is_valid():
        ctx = {"form": form, "proposal": proposal, "form_errors": form.errors}
        return render(request, "proposals/vote.html", ctx)

    # Valid Form
    vote_value = form.cleaned_data["vote_value"]
    comment = form.cleaned_data["comment"]

    utils.update_reviewer_vote_info(
        user, psr_vote, vote_value, comment, vote_phase, proposal, conference
    )
    return HttpResponseRedirect(reverse("proposals-to-review", args=[conference.slug]))
