# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from junction.conferences.models import ConferenceProposalReviewer
from junction.feedback.models import (
    TextFeedbackQuestion,
    ChoiceFeedbackQuestion,
    ChoiceFeedbackQuestionValue,
    ScheduleItemChoiceFeedback,
)


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):

        print('Creating conference admin group...')
        conference_admins, created = Group.objects.get_or_create(name='Conference Admins')

        models = [ConferenceProposalReviewer, TextFeedbackQuestion, ChoiceFeedbackQuestion,
                  ChoiceFeedbackQuestionValue, ScheduleItemChoiceFeedback,]

        for model in models:
            ct = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=ct)
            for permission in permissions:
                conference_admins.permissions.add(permission)
