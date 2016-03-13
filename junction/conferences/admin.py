# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Junction Stuff
from junction.base.admin import AuditAdmin

from . import models, service


class ConferenceAdmin(AuditAdmin):
    list_display = ('name', 'slug', 'start_date', 'end_date', 'status') + AuditAdmin.list_display
    prepopulated_fields = {'slug': ('name',), }

    def get_queryset(self, request):
        qs = super(ConferenceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(moderators=request.user)


class ConferenceModeratorAdmin(AuditAdmin):
    list_display = ('conference', 'moderator', 'active') + AuditAdmin.list_display
    list_filter = ('conference',)

    def get_queryset(self, request):
        qs = super(ConferenceModeratorAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(conference__in=[m.conference for m in moderators])


class ConferenceProposallReviewerAdmin(AuditAdmin, SimpleHistoryAdmin):
    list_display = ('conference', 'reviewer', 'active') + AuditAdmin.list_display
    list_filter = ('conference',)

    def get_queryset(self, request):
        qs = super(ConferenceProposallReviewerAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(conference__in=[m.conference for m in moderators])


class ConferenceSettingAdmin(AuditAdmin, SimpleHistoryAdmin):
    list_display = ('conference', 'name', 'value') + AuditAdmin.list_display
    list_filter = ('conference',)

    def get_queryset(self, request):
        qs = super(ConferenceSettingAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(conference__in=[m.conference for m in moderators])


admin.site.register(models.Conference, ConferenceAdmin)
admin.site.register(models.ConferenceModerator, ConferenceModeratorAdmin)
admin.site.register(models.ConferenceProposalReviewer,
                    ConferenceProposallReviewerAdmin)
admin.site.register(models.ConferenceVenue)
admin.site.register(models.Room)
admin.site.register(models.ConferenceSetting, ConferenceSettingAdmin)
