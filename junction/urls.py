# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import django.views.defaults
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView, TemplateView
from rest_framework import routers

import junction.proposals.dashboard
from junction.conferences import views as conference_views
from junction.devices.views import DeviceDetailApiView, DeviceListApiView
from junction.feedback.views import (
    FeedbackListApiView,
    FeedbackQuestionListApiView,
    view_feedback,
)
from junction.proposals import views as proposal_views
from junction.schedule import views as schedule_views
from junction.schedule.views import non_proposal_schedule_item_view

from .views import HomePageView

router = routers.DefaultRouter()

router.register("conferences", conference_views.ConferenceView)
router.register("venues", conference_views.VenueView)
router.register("rooms", conference_views.RoomView)

router.register("proposals", proposal_views.ProposalView)

router.register("schedules", schedule_views.ScheduleView)

"""
Root url routering file.

You should put the url config in their respective app putting only a
reference to them here.
"""


urlpatterns = [
    url(r"^$", HomePageView.as_view(), name="page-home"),
    # Django Admin
    url(r"^nimda/", admin.site.urls),
    # Third Party Stuff
    url(r"^accounts/", include("allauth.urls")),

    # Tickets
    url(r"^tickets/", include("junction.tickets.urls")),
    url(
        r"^feedback/(?P<schedule_item_id>\d+)/$", view_feedback, name="feedback-detail"
    ),
    url(
        r"^schedule_item/(?P<sch_item_id>\d+)/$",
        non_proposal_schedule_item_view,
        name="schedule-item",
    ),
    url(r"^api/v1/", include(router.urls)),
    # Device
    url(r"^api/v1/devices/$", DeviceListApiView.as_view(), name="device-list"),
    url(
        r"^api/v1/devices/(?P<_uuid>[\w-]+)/$",
        DeviceDetailApiView.as_view(),
        name="device-detail",
    ),
    # Feedback
    url(
        "^api/v1/feedback_questions/$",
        FeedbackQuestionListApiView.as_view(),
        name="feedback-questions-list",
    ),
    url("^api/v1/feedback/$", FeedbackListApiView.as_view(), name="feedback-list"),
    # User Dashboard
    url(r"^profiles/", include("junction.profiles.urls", namespace="profiles")),
    # Static Pages. TODO: to be refactored
    url(
        r"^speakers/$",
        TemplateView.as_view(template_name="static-content/speakers.html",),
        name="speakers-static",
    ),
    url(
        r"^schedule/$",
        TemplateView.as_view(template_name="static-content/schedule.html",),
        name="schedule-static",
    ),
    url(
        r"^venue/$",
        TemplateView.as_view(template_name="static-content/venue.html",),
        name="venue-static",
    ),
    url(
        r"^sponsors/$",
        TemplateView.as_view(template_name="static-content/sponsors.html",),
        name="sponsors-static",
    ),
    url(
        r"^blog/$",
        TemplateView.as_view(template_name="static-content/blog-archive.html",),
        name="blog-archive",
    ),
    url(
        r"^coc/$",
        TemplateView.as_view(template_name="static-content/coc.html",),
        name="coc-static",
    ),
    url(
        r"^faq/$",
        TemplateView.as_view(template_name="static-content/faq.html",),
        name="faq-static",
    ),
    # Conference Pages
    url(r"^(?P<conference_slug>[\w-]+)/", include("junction.conferences.urls")),
    # Proposals related
    url(r"^(?P<conference_slug>[\w-]+)/proposals/", include("junction.proposals.urls")),
    url(
        r"^(?P<conference_slug>[\w-]+)/dashboard/reviewers/",
        junction.proposals.dashboard.reviewer_comments_dashboard,
        name="proposal-reviewers-dashboard",
    ),
    url(
        r"^(?P<conference_slug>[\w-]+)/dashboard/proposal_state/$",
        junction.proposals.dashboard.proposal_state,
        name="proposal-state",
    ),
    url(
        r"^(?P<conference_slug>[\w-]+)/dashboard/$",
        junction.proposals.dashboard.proposals_dashboard,
        name="proposal-dashboard",
    ),
    url(
        r"^(?P<conference_slug>[\w-]+)/dashboard/votes/$",
        junction.proposals.dashboard.reviewer_votes_dashboard,
        name="proposal-reviewer-votes-dashboard",
    ),
    url(
        r"^(?P<conference_slug>[\w-]+)/dashboard/votes/export/$",
        junction.proposals.dashboard.export_reviewer_votes,
        name="export-reviewer-votes",
    ),
    # Schedule related
    url(r"^(?P<conference_slug>[\w-]+)/schedule/", include("junction.schedule.urls")),
    # Proposals as conference home page. TODO: Needs to be enhanced
    url(
        r"^(?P<conference_slug>[\w-]+)/",
        RedirectView.as_view(pattern_name="proposals-list"),
        name="conference-detail",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        url(r"^400/$", django.views.defaults.bad_request),  # noqa
        url(r"^403/$", django.views.defaults.permission_denied),
        url(r"^404/$", django.views.defaults.page_not_found),
        url(r"^500/$", django.views.defaults.server_error),
    ]
