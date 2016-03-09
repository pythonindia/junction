# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Standard Library
import datetime
import random

# Third Party Stuff
import six
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now
from sampledatahelper.helper import SampleDataHelper

# Junction Stuff
from junction.base import constants
from junction.conferences.models import Conference
from junction.proposals.models import (
    Proposal,
    ProposalComment,
    ProposalSection,
    ProposalSectionReviewerVoteValue,
    ProposalType
)
from junction.schedule.models import ScheduleItem

NUM_USERS = getattr(settings, "NUM_USERS", 10)
NUM_CONFERENCES = getattr(settings, "NUM_CONFERENCES", 4)
NUM_EMPTY_CONFERENCES = getattr(settings, "NUM_EMPTY_CONFERENCES", 2)
NUM_PROPOSAL_SECTIONS = getattr(settings, "NUM_PROPOSAL_SECTIONS", 5)
NUM_PROPOSAL_TYPES = getattr(settings, "NUM_PROPOSAL_TYPES", 8)
NUM_PUBLIC_PROPOSALS = getattr(settings, "NUM_PUBLIC_PROPOSALS", 20)
NUM_DRAFT_PROPOSALS = getattr(settings, "NUM_DRAFT_PROPOSALS", 7)
NUM_CANCELLED_PROPOSALS = getattr(settings, "NUM_CANCELLED_PROPOSALS", 7)
NUM_PUBLIC_COMMENTS = getattr(settings, "NUM_PUBLIC_COMMENTS", 10)
NUM_REVIEWER_COMMENTS = getattr(settings, "NUM_REVIEWER_COMMENTS", 10)


class Command(BaseCommand):
    sd = SampleDataHelper(seed=12345678901)

    @transaction.atomic
    def handle(self, *args, **options):

        self.users = []
        self.conferences = []
        self.proposals = []
        self.proposal_reviewers = []

        print('  Updating domain to localhost:8000')  # Update site url
        site = Site.objects.get_current()
        site.domain, site.name = 'localhost:8000', 'Local'
        site.save()

        print('  Creating Superuser')  # create superuser
        super_user = self.create_user(is_superuser=True, username='admin',
                                      is_active=True)
        EmailAddress.objects.get_or_create(user=super_user,
                                           verified=True,
                                           primary=True,
                                           email=super_user.email)

        print('  Creating sample Users')  # create users
        for x in range(NUM_USERS):
            self.users.append(self.create_user(counter=x))

        print('  Creating proposal sections')
        self.proposal_sections = self.create_proposal_sections()

        print('  Create proposal types')
        self.proposal_types = self.create_proposal_types()

        # create conferences
        print('  Creating sample Conferences')
        for x in range(NUM_CONFERENCES + NUM_EMPTY_CONFERENCES):
            conference = self.create_conference(x)
            self.conferences.append(conference)

            if x < NUM_CONFERENCES:
                self.create_moderators(conference)
                self.proposal_reviewers = self.create_propsoal_reviewers(conference)

                # attach all proposal sections
                for section in self.proposal_sections:
                    conference.proposal_sections.add(section)

                # attach all proposal types
                for proposal_type in self.proposal_types:
                    conference.proposal_types.add(proposal_type)

        # create proposals
        print('  Creating sample proposals')
        for x in range(NUM_PUBLIC_PROPOSALS):
            self.proposals.append(self.create_proposal(proposal_type="Public"))

        for x in range(NUM_DRAFT_PROPOSALS):
            self.proposals.append(self.create_proposal(proposal_type="Draft"))

        for x in range(NUM_CANCELLED_PROPOSALS):
            self.proposals.append(self.create_proposal(proposal_type="Cancelled"))

        print('  Create sample Schedule')
        for proposal in self.proposals:
            if not proposal.get_status_display() == 'Public':
                continue
            self.create_scheduled_item(proposal=proposal)
        self.create_scheduled_item(proposal='Break',
                                   conference=self.conferences[0])

        # create comments
        print('  Creating sample proposal comments')
        for x in range(NUM_PUBLIC_COMMENTS):
            self.create_proposal_comment(users=self.users)

        reviewers = [i.reviewer for i in self.proposal_reviewers]
        for x in range(NUM_REVIEWER_COMMENTS):
            self.create_proposal_comment(users=reviewers)

        print(' Creating default choices for proposal reviewer vote values.')
        for vote in constants.ProposalReviewVote.CHOICES:
            ProposalSectionReviewerVoteValue.objects.create(vote_value=vote[0], description=vote[1])

    def create_proposal_sections(self):
        sections = []
        for count in range(NUM_PROPOSAL_SECTIONS):
            sections.append(ProposalSection.objects.create(**{
                'name': "Proposal Section %d" % count,
                'description': "Proposal Section %d description" % count,
                'active': True
            }))
        return sections

    def create_proposal_types(self):
        types = []
        for count in range(NUM_PROPOSAL_TYPES):
            types.append(ProposalType.objects.create(**{
                'name': "Proposal Type %d" % count,
                'description': "Proposal Section %d description" % count,
                'active': True
            }))
        return types

    def create_moderators(self, conference):
        moderators = []
        count = self.sd.int(1, len(self.users))
        for user in random.sample(self.users, count):
            moderators.append(conference.moderators.create(
                moderator=user, active=self.sd.boolean()))
        return moderators

    def create_propsoal_reviewers(self, conference):
        proposal_reviewers = []
        count = self.sd.int(1, len(self.users))
        for user in random.sample(self.users, count):
            proposal_reviewers.append(conference.proposal_reviewers.create(
                reviewer=user, active=self.sd.boolean()))
        return proposal_reviewers

    def create_scheduled_item(self, proposal, conference=None):
        kwargs = {}
        kwargs['conference'] = conference if conference \
            else proposal.conference
        kwargs['event_date'] = kwargs['conference'].start_date
        kwargs['start_time'] = datetime.datetime.time(datetime.datetime.now())
        kwargs['end_time'] = datetime.datetime.time(
            datetime.datetime.now() + datetime.timedelta(minutes=45))
        if isinstance(proposal, six.string_types):
            ScheduleItem.objects.create(
                alt_name=proposal,
                **kwargs)
        else:
            ScheduleItem.objects.create(
                session=proposal,
                **kwargs)

    def create_conference(self, counter, start_date=None, end_date=None):
        if counter == 0:
            min_days_from_creation = 30

            start_date = now() + datetime.timedelta(
                days=min_days_from_creation)
            # 2 day conference
            end_date = now() + datetime.timedelta(
                days=min_days_from_creation + 2)
        else:
            start_date = start_date or now() + datetime.timedelta(
                random.randrange(-55, 55))
            end_date = end_date or start_date + datetime.timedelta(
                random.randrange(1, 4))

        conference = Conference.objects.create(
            name='%s Conference' % self.sd.words(1, 2).title(),
            description=self.sd.paragraph(),
            status=self.sd.choices_key(constants.ConferenceStatus.CHOICES),
            start_date=start_date,
            end_date=end_date,
            created_by=self.sd.choice(self.users),
            modified_by=self.sd.choice(self.users))

        return conference

    def create_user(self, counter=None, username=None, email=None, **kwargs):
        counter = counter or self.sd.int()
        params = {
            "username": username or 'user{0}'.format(counter),
            "first_name": kwargs.get('first_name', self.sd.name("us", 1)),
            "last_name": kwargs.get('last_name', self.sd.surname("us", 1)),
            "email": email or self.sd.email(),
            "is_active": kwargs.get('is_active', self.sd.boolean()),
            "is_superuser": kwargs.get('is_superuser', False),
            "is_staff": kwargs.get('is_staff', kwargs.get('is_superuser', self.sd.boolean())),
        }
        user = get_user_model().objects.create(**params)
        password = '123123'

        user.set_password(password)
        user.save()

        print("User created with username: {username} and password: {password}".format(
            username=params.get('username'), password=password))

        return user

    def create_proposal(self, proposal_type):

        status = next((i[0] for i in constants.ProposalStatus.CHOICES if
                       i[1] == proposal_type))

        proposal = Proposal.objects.create(
            conference=self.sd.choice(self.conferences),
            proposal_section=self.sd.choice(self.proposal_sections),
            proposal_type=self.sd.choice(self.proposal_types),
            author=self.sd.choice(self.users),
            title='%s Proposal' % self.sd.words(1, 2).title(),
            description=self.sd.paragraph(),
            status=status,
            deleted=self.sd.boolean())

        return proposal

    def create_proposal_comment(self, users):

        commenter = self.sd.choice(users)

        comment = ProposalComment.objects.create(
            proposal=self.sd.choice(self.proposals),
            private=self.sd.boolean(),
            comment='Comment',
            commenter=commenter)

        return comment
