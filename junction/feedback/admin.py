# -*- coding: utf-8 -*-

# Third Party Stuff
from django.contrib import admin

# Junction Stuff
from junction.base.admin import TimeAuditAdmin
from junction.conferences import service

from .models import (
    ChoiceFeedbackQuestion,
    ChoiceFeedbackQuestionValue,
    ScheduleItemChoiceFeedback,
    ScheduleItemTextFeedback,
    TextFeedbackQuestion
)


# Register your models here.


class TextFeedbackQuestionAdmin(TimeAuditAdmin):
    list_display = ('title', 'schedule_item_type', 'conference') + \
                   TimeAuditAdmin.list_display  # noqa

    def get_queryset(self, request):
        qs = super(TextFeedbackQuestionAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(conference__in=[m.conference for m in moderators])


class ChoiceFeedbackQuestionAdmin(TimeAuditAdmin):
    list_display = ('title', 'schedule_item_type', 'conference') + \
                   TimeAuditAdmin.list_display  # noqa

    def get_queryset(self, request):
        qs = super(ChoiceFeedbackQuestionAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(conference__in=[m.conference for m in moderators])


class ChoiceFeedbackQuestionValueAdmin(TimeAuditAdmin):
    list_display = ('question', 'title', 'value') + \
                   TimeAuditAdmin.list_display  # noqa

    def get_queryset(self, request):
        qs = super(ChoiceFeedbackQuestionValueAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(question__conference__in=[m.conference
                                                   for m in moderators])


class ScheduleItemTextFeedbackAdmin(TimeAuditAdmin):
    list_display = ('schedule_item', 'question', 'text', 'device') + \
                   TimeAuditAdmin.list_display  # noqa
    list_filter = ['schedule_item']  # noqa

    def get_queryset(self, request):
        qs = super(ScheduleItemTextFeedbackAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(question__conference__in=[m.conference
                                                   for m in moderators])


class ScheduleItemChoiceFeedbackAdmin(TimeAuditAdmin):
    list_display = ('schedule_item', 'question', 'value', 'device') + \
                   TimeAuditAdmin.list_display  # noqa
    list_filter = ['schedule_item']  # noqa

    def get_queryset(self, request):
        qs = super(ScheduleItemChoiceFeedbackAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(question__conference__in=[m.conference
                                                   for m in moderators])


admin.site.register(TextFeedbackQuestion, TextFeedbackQuestionAdmin)
admin.site.register(ChoiceFeedbackQuestion, ChoiceFeedbackQuestionAdmin)
admin.site.register(ChoiceFeedbackQuestionValue,
                    ChoiceFeedbackQuestionValueAdmin)
admin.site.register(ScheduleItemTextFeedback, ScheduleItemTextFeedbackAdmin)
admin.site.register(ScheduleItemChoiceFeedback,
                    ScheduleItemChoiceFeedbackAdmin)
