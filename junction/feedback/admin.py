# -*- coding: utf-8 -*-

from django.contrib import admin

from junction.base.admin import TimeAuditAdmin
from .models import (TextFeedbackQuestion,
                     ChoiceFeedbackQuestion,
                     ChoiceFeedbackQuestionValue,
                     ScheduleItemTextFeedback,
                     ScheduleItemChoiceFeedback)

# Register your models here.


class TextFeedbackQuestionAdmin(TimeAuditAdmin):
    list_display = ('title', 'schedule_item_type', 'conference') + \
                   TimeAuditAdmin.list_display  # noqa


class ChoiceFeedbackQuestionAdmin(TimeAuditAdmin):
    list_display = ('title', 'schedule_item_type', 'conference') + \
                   TimeAuditAdmin.list_display  # noqa


class ChoiceFeedbackQuestionValueAdmin(TimeAuditAdmin):
    list_display = ('question', 'title', 'value') + \
                   TimeAuditAdmin.list_display  # noqa


class ScheduleItemTextFeedbackAdmin(TimeAuditAdmin):
    list_display = ('schedule_item', 'question', 'text', 'device') + \
                   TimeAuditAdmin.list_display  # noqa
    list_filter = ['schedule_item']  # noqa


class ScheduleItemChoiceFeedbackAdmin(TimeAuditAdmin):
    list_display = ('schedule_item', 'question', 'value', 'device') + \
                   TimeAuditAdmin.list_display  # noqa
    list_filter = ['schedule_item']  # noqa


admin.site.register(TextFeedbackQuestion, TextFeedbackQuestionAdmin)
admin.site.register(ChoiceFeedbackQuestion, ChoiceFeedbackQuestionAdmin)
admin.site.register(ChoiceFeedbackQuestionValue,
                    ChoiceFeedbackQuestionValueAdmin)
admin.site.register(ScheduleItemTextFeedback, ScheduleItemTextFeedbackAdmin)
admin.site.register(ScheduleItemChoiceFeedback,
                    ScheduleItemChoiceFeedbackAdmin)
