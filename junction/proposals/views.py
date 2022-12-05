# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import collections

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.http import Http404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from hashids import Hashids
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.response import Response

from junction.base.constants import (
    ConferenceSettingConstants,
    ConferenceStatus,
    ProposalReviewStatus,
    ProposalStatus,
)
from junction.conferences.models import Conference
from junction.feedback import permissions as feedback_permission

from . import permissions, serializers
from .forms import (
    ProposalCommentForm,
    ProposalForm,
    ProposalReviewForm,
    ProposalsToReviewForm,
)
from .models import Proposal, ProposalComment, ProposalSectionReviewer, ProposalVote
from .services import send_mail_for_new_proposal, send_mail_for_proposal_content


class ProposalView(viewsets.ReadOnlyModelViewSet):
    queryset = Proposal.objects.filter(status=2)
    serializer_class = serializers.ProposalSerializer
    filter_backend = (filters.DjangoFilterBackend,)
    filter_fields = ("conference", "review_status", "proposal_type", "proposal_section")

    def get_queryset(self):
        data = super(ProposalView, self).get_queryset()
        return self.filter_queryset(data)

    def list(self, request):
        data = self.get_queryset()
        response = {"proposals": []}
        for datum in data:
            d = datum.to_response(request=request)
            response["proposals"].append(d)
        return Response(response)


# Filtering
def _filter_proposals(request, proposals_qs):
    """Filters a proposal queryset based on the values present in the request's
    query strings.

    Supported query strings are `proposal_section` and `proposal_type`.
    """
    serializer = serializers.ProposalFilterSerializer(data=request.GET)
    if not serializer.is_valid():
        raise Http404()

    proposal_section_filter = serializer.validated_data.get("proposal_section", None)
    proposal_type_filter = serializer.validated_data.get("proposal_type", None)
    is_filtered = False
    filter_name = False

    if proposal_section_filter:
        proposals_qs = proposals_qs.filter(proposal_section=proposal_section_filter)
        is_filtered = True
        filter_name = proposal_section_filter

    if proposal_type_filter:
        proposals_qs = proposals_qs.filter(proposal_type=proposal_type_filter)
        is_filtered = True
        filter_name = proposal_type_filter

    return is_filtered, filter_name, proposals_qs


@require_http_methods(["GET"])
def list_proposals(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    public_voting = ConferenceSettingConstants.ALLOW_PUBLIC_VOTING_ON_PROPOSALS
    public_voting_setting = conference.conferencesetting_set.filter(
        name=public_voting["name"]
    ).first()
    public_voting_setting_value = (
        public_voting_setting.value if public_voting_setting else True
    )

    proposals_qs = Proposal.objects.filter(conference=conference).select_related(
        "proposal_type", "proposal_section", "conference", "author",
    )

    is_filtered, filter_name, proposals_qs = _filter_proposals(request, proposals_qs)

    # make sure it's after the tag filtering is applied
    selected_proposals_list = proposals_qs.filter(
        review_status=ProposalReviewStatus.SELECTED
    )

    selected_proposals = collections.defaultdict(list)
    for proposal in selected_proposals_list:
        name = proposal.proposal_type.name
        selected_proposals[name].append(proposal)

    # Display proposals which are public
    public_proposals_list = (
        proposals_qs.exclude(review_status=ProposalReviewStatus.SELECTED)
        .filter(status=ProposalStatus.PUBLIC)
        .order_by("created_at")
    )

    return render(
        request,
        "proposals/list.html",
        {
            "public_proposals_list": public_proposals_list,
            "selected_proposals": dict(selected_proposals),
            "proposal_sections": conference.proposal_sections.all(),
            "proposal_types": conference.proposal_types.all(),
            "is_filtered": is_filtered,
            "filter_name": filter_name,
            "is_reviewer": permissions.is_proposal_reviewer(
                user=request.user, conference=conference
            ),
            "conference": conference,
            "ConferenceStatus": ConferenceStatus,
            "public_voting_setting": public_voting_setting_value,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def create_proposal(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    if request.method == "GET":
        if not conference.is_accepting_proposals():
            return render(request, "proposals/closed.html", {"conference": conference})
        form = ProposalForm(
            conference, action="create", initial={"status": ProposalStatus.PUBLIC}
        )
        return render(
            request, "proposals/create.html", {"form": form, "conference": conference}
        )

    # POST Workflow
    form = ProposalForm(conference, data=request.POST, action="create")

    if not form.is_valid():
        return render(
            request,
            "proposals/create.html",
            {"form": form, "conference": conference, "errors": form.errors},
        )

    # Valid Form
    proposal = Proposal.objects.create(
        author=request.user,
        conference=conference,
        title=form.cleaned_data["title"],
        description=form.cleaned_data["description"],
        target_audience=form.cleaned_data["target_audience"],
        prerequisites=form.cleaned_data["prerequisites"],
        video_url=form.cleaned_data["video_url"],
        content_urls=form.cleaned_data["content_urls"],
        private_content_urls=form.cleaned_data["private_content_urls"],
        speaker_info=form.cleaned_data["speaker_info"],
        speaker_links=form.cleaned_data["speaker_links"],
        is_first_time_speaker=form.cleaned_data["is_first_time_speaker"],
        status=form.cleaned_data["status"],
        proposal_type_id=form.cleaned_data["proposal_type"],
        proposal_section_id=form.cleaned_data["proposal_section"],
    )
    host = "{}://{}".format(settings.SITE_PROTOCOL, request.META.get("HTTP_HOST"))

    if settings.USE_ASYNC_FOR_EMAIL:
        send_mail_for_new_proposal.delay(proposal.id, host)
    else:
        send_mail_for_new_proposal(proposal.id, host)

    return HttpResponseRedirect(
        reverse("proposal-detail", args=[conference.slug, proposal.slug])
    )


@require_http_methods(["GET"])
def detail_proposal(request, conference_slug, slug, hashid=None):
    """Display a proposal detail page.
    """
    # Here try to get a proposal by it's hashid. If the slug didn't match because
    # the title might have changed, redirect to the correct slug.
    # hashid is optional due to backward compatibility. If the hashid is not present
    # we still try to get the proposal by old method i.e. using just the slug, but
    # redirect to the correct url containing hashid.
    hashids = Hashids(min_length=5)
    id = hashids.decode(hashid)
    if id:
        proposal = get_object_or_404(Proposal, id=id[0])
        if slug != proposal.get_slug():
            return HttpResponseRedirect(proposal.get_absolute_url())
    else:
        conference = get_object_or_404(Conference, slug=conference_slug)
        proposal = get_object_or_404(Proposal, slug=slug, conference=conference)
        return HttpResponseRedirect(proposal.get_absolute_url())

    if proposal.deleted or (
        not proposal.is_public() and request.user != proposal.author
    ):
        raise Http404("404")

    # Here we have obtained the proposal that we want to display.
    conference = proposal.conference
    read_private_comment = permissions.is_proposal_author_or_proposal_reviewer(
        request.user, conference, proposal
    )
    write_private_comment = permissions.is_proposal_author_or_proposal_section_reviewer(
        request.user, conference, proposal
    )
    is_reviewer = permissions.is_proposal_reviewer(request.user, conference)
    is_section_reviewer = permissions.is_proposal_section_reviewer(
        request.user, conference, proposal
    )
    public_voting = ConferenceSettingConstants.ALLOW_PUBLIC_VOTING_ON_PROPOSALS
    public_voting_setting = conference.conferencesetting_set.filter(
        name=public_voting["name"]
    ).first()
    vote_value, public_voting_setting_value = 0, True

    if public_voting_setting:
        public_voting_setting_value = public_voting_setting.value
        try:
            if request.user.is_authenticated:
                proposal_vote = ProposalVote.objects.get(
                    proposal=proposal, voter=request.user
                )
                vote_value = 1 if proposal_vote.up_vote else -1
        except ProposalVote.DoesNotExist:
            pass

    ctx = {
        "login_url": settings.LOGIN_URL,
        "proposal": proposal,
        "read_private_comment": read_private_comment,
        "write_private_comment": write_private_comment,
        "vote_value": vote_value,
        "is_author": request.user == proposal.author,
        "is_reviewer": is_reviewer,
        "is_section_reviewer": is_section_reviewer,
        "can_view_feedback": False,
        "can_vote": permissions.is_proposal_voting_allowed(proposal),
        "public_voting_setting": public_voting_setting_value,
    }

    if proposal.scheduleitem_set.all():
        schedule_item = proposal.scheduleitem_set.all()[0]
        ctx["can_view_feedback"] = feedback_permission.can_view_feedback(
            user=request.user, schedule_item=schedule_item
        )
        ctx["schedule_item"] = schedule_item

    comments = ProposalComment.objects.filter(
        proposal=proposal, deleted=False, vote=False
    )

    if read_private_comment:
        ctx["reviewers_comments"] = comments.get_reviewers_comments()
    if write_private_comment:
        ctx["reviewers_proposal_comment_form"] = ProposalCommentForm(
            initial={"private": True}
        )
    if is_reviewer:
        ctx["reviewers_only_proposal_comment_form"] = ProposalCommentForm(
            initial={"reviewer": True}
        )
        ctx["reviewers_only_comments"] = comments.get_reviewers_only_comments()

    ctx.update(
        {
            "comments": comments.get_public_comments(),
            "proposal_comment_form": ProposalCommentForm(),
        }
    )

    ctx["enable_upload_content"] = settings.ENABLE_UPLOAD_CONTENT
    ctx["enable_second_phase_voting"] = settings.ENABLE_SECOND_PHASE_VOTING

    return render(request, "proposals/detail/base.html", ctx)


@login_required
@require_http_methods(["GET", "POST"])
def update_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not permissions.is_proposal_author(user=request.user, proposal=proposal):
        raise PermissionDenied

    if request.method == "GET":
        form = ProposalForm.populate_form_for_update(proposal)
        return render(
            request, "proposals/update.html", {"form": form, "proposal": proposal}
        )

    # POST Workflow
    form = ProposalForm(conference, data=request.POST)
    if not form.is_valid():
        return render(
            request,
            "proposals/update.html",
            {"form": form, "proposal": proposal, "errors": form.errors},
        )

    # Valid Form
    proposal.title = form.cleaned_data["title"]
    proposal.description = form.cleaned_data["description"]
    proposal.target_audience = form.cleaned_data["target_audience"]
    proposal.prerequisites = form.cleaned_data["prerequisites"]
    proposal.video_url = form.cleaned_data["video_url"]
    proposal.content_urls = form.cleaned_data["content_urls"]
    proposal.private_content_urls = form.cleaned_data["private_content_urls"]
    proposal.speaker_info = form.cleaned_data["speaker_info"]
    proposal.speaker_links = form.cleaned_data["speaker_links"]
    proposal.is_first_time_speaker = form.cleaned_data["is_first_time_speaker"]
    proposal.status = form.cleaned_data["status"]
    proposal.proposal_type_id = form.cleaned_data["proposal_type"]
    proposal.proposal_section_id = form.cleaned_data["proposal_section"]
    proposal.save()
    return HttpResponseRedirect(
        reverse("proposal-detail", args=[conference.slug, proposal.slug])
    )


@login_required
@require_http_methods(["GET", "POST"])
def proposals_to_review(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)

    if not permissions.is_proposal_reviewer(request.user, conference):
        raise PermissionDenied

    proposals_qs = (
        Proposal.objects.select_related(
            "proposal_type", "proposal_section", "conference", "author",
        )
        .filter(conference=conference)
        .filter(status=ProposalStatus.PUBLIC)
        .order_by("created_at")
    )
    psr = ProposalSectionReviewer.objects.filter(
        conference_reviewer__reviewer=request.user,
        conference_reviewer__conference=conference,
    )
    proposal_reviewer_sections = [p.proposal_section for p in psr]
    proposal_sections = conference.proposal_sections.all()
    proposal_types = conference.proposal_types.all()

    s_items = collections.namedtuple("section_items", "section proposals")

    if request.method == "GET":
        proposals_to_review = []
        for section in proposal_reviewer_sections:
            section_proposals = [
                p for p in proposals_qs if p.proposal_section == section
            ]
            proposals_to_review.append(s_items(section, section_proposals))

        form = ProposalsToReviewForm(
            conference=conference, proposal_sections=proposal_reviewer_sections
        )

        context = {
            "proposals_to_review": proposals_to_review,
            "proposal_reviewer_sections": proposal_reviewer_sections,
            "proposal_sections": proposal_sections,
            "proposal_types": proposal_types,
            "conference": conference,
            "form": form,
        }

        return render(request, "proposals/to_review.html", context)

    # POST Workflow
    form = ProposalsToReviewForm(
        data=request.POST,
        conference=conference,
        proposal_sections=proposal_reviewer_sections,
    )
    if not form.is_valid():
        context["errors"] = form.errors
        return render(request, "proposals/to_review.html", context)

    # Valid Form
    p_section = form.cleaned_data["proposal_section"]
    p_type = form.cleaned_data["proposal_type"]
    r_comment = form.cleaned_data["reviewer_comment"]

    if p_section != "all":
        proposals_qs = proposals_qs.filter(proposal_section__id__in=p_section)
    if p_type != "all":
        proposals_qs = proposals_qs.filter(proposal_type__id__in=p_type)
    if r_comment == "True":
        proposals_qs = [p for p in proposals_qs if p.get_reviews_comments_count() > 0]

    proposals_to_review = []
    for section in proposal_reviewer_sections:
        section_proposals = [p for p in proposals_qs if p.proposal_section == section]
        proposals_to_review.append(s_items(section, section_proposals))

    context = {
        "proposals_to_review": proposals_to_review,
        "proposal_sections": proposal_sections,
        "proposal_types": proposal_types,
        "conference": conference,
        "form": form,
    }

    return render(request, "proposals/to_review.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def review_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not permissions.is_proposal_section_reviewer(request.user, conference, proposal):
        raise PermissionDenied

    if request.method == "GET":
        comments = ProposalComment.objects.filter(proposal=proposal, deleted=False)

        proposal_review_form = ProposalReviewForm(
            initial={"review_status": proposal.review_status}
        )

        ctx = {
            "proposal": proposal,
            "proposal_review_form": proposal_review_form,
            "reviewers_comments": comments.get_reviewers_comments(),
            "reviewers_only_comments": comments.get_reviewers_only_comments(),
            "reviewers_proposal_comment_form": ProposalCommentForm(
                initial={"private": True}
            ),
            "reviewers_only_proposal_comment_form": ProposalCommentForm(
                initial={"review": True}
            ),
        }

        return render(request, "proposals/review.html", ctx)

    # POST Workflow
    form = ProposalReviewForm(data=request.POST)
    if not form.is_valid():
        context = {"form": form, "proposal": proposal, "form_errors": form.errors}
        return render(request, "proposals/review.html", context)

    # Valid Form
    proposal.review_status = form.cleaned_data["review_status"]
    proposal.save()

    return HttpResponseRedirect(reverse("proposals-list", args=[conference.slug]))


@login_required
@require_http_methods(["POST"])
def proposal_upload_content(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not (
        permissions.is_proposal_section_reviewer(request.user, conference, proposal)
        or request.user.is_superuser
    ):
        raise PermissionDenied

    host = "{}://{}".format(settings.SITE_PROTOCOL, request.META["HTTP_HOST"])

    if settings.USE_ASYNC_FOR_EMAIL:
        send_mail_for_proposal_content.delay(conference.id, proposal.id, host)
        message = "Email sent successfully."
    else:
        response = send_mail_for_proposal_content(conference.id, proposal.id, host)
        if response == 1:
            message = "Email sent successfully."
        else:
            message = (
                "There is problem in sending mail. Please contact conference chair."
            )

    return HttpResponse(message)


@login_required
@require_http_methods(["GET", "POST"])
def delete_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    permissions.is_proposal_author_or_permisson_denied(
        user=request.user, proposal=proposal
    )

    if request.method == "GET":
        return render(request, "proposals/delete.html", {"proposal": proposal})
    elif request.method == "POST":
        proposal.delete()
        return HttpResponseRedirect(reverse("proposals-list", args=[conference.slug]))
