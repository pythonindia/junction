# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


from junction.conferences.models import Conference


APP_PERMISSIONS = {'conferences': ['change_conferencesetting',
                                   'add_conferencevenue',
                                   'change_conferencevenue',
                                   'delete_conferencevenue',
                                   'change_conference',
                                   'add_conferencemoderator',
                                   'change_conferencemoderator',
                                   'delete_conferencemoderator',
                                   'add_conferencemoderator',
                                   'change_conferencemoderator',
                                   'delete_conferencemoderator',
                                   'add_conferenceproposalreviewer',
                                   'change_conferenceproposalreviewer',
                                   'delete_conferenceproposalreviewer',
                                   'add_room', 'change_room', 'delete_room'],
                   'proposals': ['add_proposalsection',
                                 'change_proposalsection',
                                 'delete_proposalsection',
                                 'add_proposalsectionreviewer',
                                 'change_proposalsectionreviewer',
                                 'delete_proposalsectionreviewer',
                                 'add_proposaltype',
                                 'change_proposaltype',
                                 'delete_proposaltype',
                                 'change_proposal',
                                 'change_proposalvote',
                                 'add_proposalsectionreviewervotevalue',
                                 'change_proposalsectionreviewervotevalue',
                                 'add_proposalsectionreviewervote',
                                 'change_proposalsectionreviewervote',
                                 'add_proposalcomment',
                                 'change_proposalcomment',
                                 'add_proposalcommentvote',
                                 'change_proposalcommentvote'],
                   'schedule': ['add_scheduleitem',
                                'change_scheduleitem',
                                'delete_scheduleitem',
                                'add_scheduleitemtype',
                                'change_scheduleitemtype',
                                'delete_scheduleitemtype'],
                   'devices': ['add_device', 'change_device',
                               'delete_device'],
                   'feedback': ['add_textfeedbackquestion',
                                'change_textfeedbackquestion',
                                'delete_textfeedbackquestion',
                                'add_choicefeedbackquestion',
                                'change_choicefeedbackquestion',
                                'delete_choicefeedbackquestion',
                                'add_scheduleitemtextfeedback',
                                'change_scheduleitemtextfeedback',
                                'delete_scheduleitemtextfeedback',
                                'add_scheduleitemchoicefeedback',
                                'change_scheduleitemchoicefeedback',
                                'delete_scheduleitemchoicefeedback',
                                'add_choicefeedbackquestionvalue',
                                'change_choicefeedbackquestionvalue',
                                'delete_choicefeedbackquestionvalue'],
                   'tickets': ['add_ticket', 'change_ticket',
                               'delete_ticket']}


class Command(BaseCommand):
    def add_argument(self, parser):
        parser.add_argument('slug', nargs=1, type=str)
        parser.add_argument('email', nargs=1, type=str)

    def has_conference(self, slug):
        try:
            conference = Conference.objects.get(slug=slug)
            return conference
        except Conference.DoesNotExist:
            raise CommandError('Conference "{}" does not exist'.format(slug))

    def create_user(self, email):
        Users = get_user_model()
        try:
            user = Users.objects.get(email=email)
            user.is_staff = True
            user.is_active = True
            user.save()
            return user
        except Users.DoesNotExist:
            raise CommandError("User '{}' doesn't exist".format(user))

    def add_permissions(self, user):
        for app_label, permissions in APP_PERMISSIONS.items():
            for perm in permissions:
                term = ".".join([app_label, perm])
                if user.has_perm(term):
                    print("User has perm: '{}'".format(term))
                else:
                    print("User doesn't have  perm: '{}'".format(term))
                    permission = Permission.objects.get(codename=perm)
                    user.user_permissions.add(permission)
                    print("Added permission '{}'".format(permission))

    def handle(self, *args, **kwargs):
        # Check conference and short circuit if missing
        if len(args) < 2:
            print("Two arguments are required")
            return
        self.has_conference(slug=args[0])
        # Check and create user
        user = self.create_user(email=args[1])
        # Add all models to user permission
        self.add_permissions(user=user)
