# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Junction Stuff
from junction.base.models import TimeAuditModel
from junction.conferences.models import Conference
from junction.devices.models import Device
from junction.schedule.models import ScheduleItem, ScheduleItemType


class BaseSessionQuestionMixin(models.Model):
    schedule_item_type = models.ForeignKey(ScheduleItemType)
    is_required = models.BooleanField(default=True)
    conference = models.ForeignKey(Conference)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class TextFeedbackQuestion(BaseSessionQuestionMixin, TimeAuditModel):
    """Store details about text feedback type information.
    """
    title = models.CharField(max_length=255,
                             verbose_name="Text Feedback Title")

    def __str__(self):
        return u"title: {}, schedule_item_type: {}, conference: {}".format(
            self.title, self.schedule_item_type, self.conference)

    def to_response(self):
        return {'title': self.title, 'id': self.id, 'type': 'text',
                'schedule_item_type': self.schedule_item_type.title,
                'is_required': self.is_required}


@python_2_unicode_compatible
class ChoiceFeedbackQuestion(BaseSessionQuestionMixin, TimeAuditModel):
    """Store details about text feedback type information.
    """
    title = models.CharField(max_length=255,
                             verbose_name="Choice Feedback Title")

    def __str__(self):
        return u"title: {}, schedule_item_type: {}, conference: {}".format(
            self.title, self.schedule_item_type, self.conference)

    def to_response(self):
        allowed_choices = [{'title': obj.title, 'value': obj.value,
                            'id': obj.id}
                           for obj in self.allowed_values.all()]
        return {'title': self.title, 'id': self.id, 'type': 'choice',
                'allowed_choices': allowed_choices,
                'schedule_item_type': self.schedule_item_type.title,
                'is_required': self.is_required}


@python_2_unicode_compatible
class ChoiceFeedbackQuestionValue(TimeAuditModel):
    """Store allowed values for each choice based question
    """
    question = models.ForeignKey(ChoiceFeedbackQuestion,
                                 related_name="allowed_values")
    title = models.CharField(max_length=255,
                             verbose_name="Choice Feedback Value Title")
    value = models.SmallIntegerField(db_index=True)

    def __str__(self):
        return u"question: {}, title: {}, value: {}".format(
            self.question, self.title, self.value)


@python_2_unicode_compatible
class ScheduleItemTextFeedback(TimeAuditModel):
    schedule_item = models.ForeignKey(ScheduleItem, db_index=True)
    question = models.ForeignKey(TextFeedbackQuestion)
    text = models.TextField()
    device = models.ForeignKey(Device, null=True, blank=True, db_index=True)

    class Meta:
        index_together = [["device", "schedule_item"]]

    def __str__(self):
        return u"schedule_item: {}, question: {}, text: {}, device: {}".format(
            self.schedule_item, self.question, self.text[:100], self.device)


@python_2_unicode_compatible
class ScheduleItemChoiceFeedback(TimeAuditModel):
    schedule_item = models.ForeignKey(ScheduleItem)
    question = models.ForeignKey(ChoiceFeedbackQuestion)
    value = models.SmallIntegerField(db_index=True)
    device = models.ForeignKey(Device, null=True, blank=True)

    class Meta:
        index_together = [["device", "schedule_item"],
                          ["schedule_item", "value"]]

    def __str__(self):
        return u"schedule_item: {}, question: {}, value: {}, device: {}".format(
            self.schedule_item, self.question, self.value, self.device)
