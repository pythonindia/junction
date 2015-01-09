# Standard Library
import random
import datetime

# Third Party Stuff
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.timezone import now
from sampledatahelper.helper import SampleDataHelper

from junction.conferences.models import Conference
from junction.custom_utils import constants

NUM_USERS = getattr(settings, "SAMPLE_DATA_NUM_USERS", 10)
NUM_CONFERENCES = getattr(settings, "SAMPLE_DATA_NUM_CONFERENCES", 4)
NUM_EMPTY_CONFERENCES = getattr(
    settings, "SAMPLE_DATA_NUM_EMPTY_CONFERENCES", 2)


class Command(BaseCommand):
    sd = SampleDataHelper(seed=12345678901)

    @transaction.atomic
    def handle(self, *args, **options):

        self.users = []

        # create superuser
        self.create_user(is_superuser=True, username='admin', is_active=True)

        # create users
        for x in range(NUM_USERS):
            self.users.append(self.create_user(counter=x))

        # create conferences
        for x in range(NUM_CONFERENCES + NUM_EMPTY_CONFERENCES):
            self.create_conference(x)

    def create_conference(self, counter, start_date=None, end_date=None):
        start_date = start_date or now() + datetime.timedelta(random.randrange(-55, 55))
        end_date = end_date or start_date + datetime.timedelta(random.randrange(1, 4))
        conference = Conference.objects.create(name='Conference Example {0}'.format(counter),
                                               description='Conference example {0} description'.format(
                                                   counter),
                                               status=self.sd.choice([i[0] for i in constants.CONFERENCE_STATUS_LIST]),
                                               start_date=start_date,
                                               end_date=end_date,
                                               created_by=self.sd.choice(self.users),
                                               modified_by=self.sd.choice(self.users),
                                               )

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
        user.set_password('123123')
        user.save()

        return user
