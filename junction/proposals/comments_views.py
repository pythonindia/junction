# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http.response import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import Http404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from junction.conferences.models import Conference

from . import permissions
from .forms import ProposalCommentForm
from .models import Proposal, ProposalComment
from .services import send_mail_for_new_comment, user_action_for_spam


@login_required
@require_http_methods(["POST"])
def create_proposal_comment(request, conference_slug, proposal_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)
    form = ProposalCommentForm(request.POST)

    if request.user.is_active is False:
        raise PermissionDenied()

    if form.is_valid():
        comment = form.cleaned_data["comment"]
        private = form.cleaned_data["private"]
        reviewer = form.cleaned_data["reviewer"]

        has_perm = permissions.is_proposal_author_or_proposal_section_reviewer(
            user=request.user, conference=conference, proposal=proposal
        )

        if private and not has_perm:
            raise Http404()

        proposal_comment = ProposalComment.objects.create(
            proposal=proposal,
            comment=comment,
            private=private,
            reviewer=reviewer,
            commenter=request.user,
        )
        host = "{}://{}".format(settings.SITE_PROTOCOL, request.META.get("HTTP_HOST"))

        if settings.USE_ASYNC_FOR_EMAIL:
            send_mail_for_new_comment.delay(proposal_comment.id, host)
        else:
            send_mail_for_new_comment(proposal_comment.id, host)

    redirect_url = reverse("proposal-detail", args=[conference.slug, proposal.slug])

    if private:
        redirect_url += "#js-reviewers"
    elif reviewer:
        redirect_url += "#js-only-reviewers"
    else:
        redirect_url += "#js-comments"

    return HttpResponseRedirect(redirect_url)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def mark_comment_as_spam(request, conference_slug, proposal_slug, proposal_comment_id):
    if not request.is_ajax() or request.user.is_active is False:
        return HttpResponseForbidden()

    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)
    proposal_comment = get_object_or_404(
        ProposalComment, proposal=proposal, id=proposal_comment_id
    )

    if proposal_comment.is_spam:
        return HttpResponse("Already marked as spam")

    proposal_comment.is_spam = True
    proposal_comment.marked_as_spam_by = request.user
    proposal_comment.save()

    user_action_for_spam(
        proposal_comment.commenter, getattr(settings, "USER_SPAM_THRESHOLD", 2)
    )

    return HttpResponse("Marked as spam")


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def unmark_comment_as_spam(
    request, conference_slug, proposal_slug, proposal_comment_id
):
    if not request.is_ajax() or request.user.is_active is False:
        return HttpResponseForbidden()

    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)
    proposal_comment = get_object_or_404(
        ProposalComment, proposal=proposal, id=proposal_comment_id
    )

    if proposal_comment.is_spam and proposal_comment.marked_as_spam_by == request.user:
        proposal_comment.is_spam = False
        proposal_comment.marked_as_spam_by = None
        proposal_comment.save()

        user_action_for_spam(
            proposal_comment.commenter, getattr(settings, "USER_SPAM_THRESHOLD", 2)
        )

        return HttpResponse("Unmarked as spam")

    return HttpResponseForbidden()
