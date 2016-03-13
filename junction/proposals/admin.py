# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget
from simple_history.admin import SimpleHistoryAdmin

# Junction Stuff
from junction.base.admin import AuditAdmin, TimeAuditAdmin
from junction.conferences import service
from junction.proposals.models import (
    Proposal,
    ProposalComment,
    ProposalCommentVote,
    ProposalSection,
    ProposalSectionReviewer,
    ProposalSectionReviewerVote,
    ProposalSectionReviewerVoteValue,
    ProposalType,
    ProposalVote
)


class ProposalSectionAdmin(AuditAdmin):
    list_display = ('name', 'active') + AuditAdmin.list_display


class ProposalSectionReviewerAdmin(AuditAdmin):
    list_display = ('conference_reviewer', 'proposal_section') + AuditAdmin.list_display
    list_filter = ['proposal_section']

    def get_queryset(self, request):
        qs = super(ProposalSectionReviewerAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(
            conference_reviewer__conference__in=[m.conference
                                                 for m in moderators])


class ProposalTypeAdmin(AuditAdmin):
    list_display = ('name', 'active', 'start_date', 'end_date') + AuditAdmin.list_display


class ProposalAdmin(TimeAuditAdmin, SimpleHistoryAdmin):
    list_display = ('proposal_info', 'author_info', 'author_email', 'conference',
                    'status', 'review_status', )
    list_filter = ['proposal_section__name', 'proposal_type',
                   'target_audience', 'conference', 'status', 'review_status']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def proposal_info(self, obj):
        return '%s (%s)' % (obj.title, obj.proposal_type)

    def author_email(self, obj):
        if obj.author:
            return obj.author.email

    def author_info(self, obj):
        if obj.author:
            return "%s (%s)" % (obj.author.get_full_name(), obj.author.username)

    def get_queryset(self, request):
        qs = super(ProposalAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(conference__in=[m.conference
                                         for m in moderators])


class ProposalVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal', 'voter', 'role', 'up_vote') + \
        TimeAuditAdmin.list_display

    def get_queryset(self, request):
        qs = super(ProposalVoteAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(proposal__conference__in=[m.conference
                                                   for m in moderators])


class ProposalSectionReviewerVoteValueAdmin(AuditAdmin):
    list_display = ('vote_value', 'description') + AuditAdmin.list_display


class ProposalSectionReviewerVoteAdmin(TimeAuditAdmin):
    list_filter = ['vote_value', 'proposal__proposal_type__name']
    list_display = ('proposal', 'voter', 'role', 'vote_value') + \
        TimeAuditAdmin.list_display

    def get_queryset(self, request):
        qs = super(ProposalSectionReviewerVoteAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(proposal__conference__in=[m.conference
                                                   for m in moderators])


class ProposalCommentAdmin(TimeAuditAdmin):
    list_display = (
        'proposal', 'commenter', 'private', 'comment') + TimeAuditAdmin.list_display
    list_filter = ['private', 'reviewer']

    def get_queryset(self, request):
        qs = super(ProposalCommentAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(proposal__conference__in=[m.conference
                                                   for m in moderators])


class ProposalCommentVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal_comment', 'voter', 'up_vote') + \
        TimeAuditAdmin.list_display

    def get_queryset(self, request):
        qs = super(ProposalCommentVoteAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(proposal_comment__proposal__conference__in=[
            m.conference for m in moderators])

admin.site.register(ProposalSection, ProposalSectionAdmin)
admin.site.register(ProposalType, ProposalTypeAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(ProposalVote, ProposalVoteAdmin)
admin.site.register(ProposalSectionReviewerVote, ProposalSectionReviewerVoteAdmin)
admin.site.register(ProposalSectionReviewerVoteValue, ProposalSectionReviewerVoteValueAdmin)
admin.site.register(ProposalComment, ProposalCommentAdmin)
admin.site.register(ProposalCommentVote, ProposalCommentVoteAdmin)
admin.site.register(ProposalSectionReviewer, ProposalSectionReviewerAdmin)
