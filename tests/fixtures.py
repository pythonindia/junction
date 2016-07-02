# -*- coding: utf-8 -*-
# Standard Library
import functools
import datetime

# Third Party Stuff
import mock
import pytest

from junction.base.constants import ConferenceStatus
from junction.conferences.models import ConferenceProposalReviewer
from junction.proposals.models import ProposalSectionReviewer

from . import factories


class Object:
    pass


@pytest.fixture
def object():
    return Object()


class PartialMethodCaller:
    def __init__(self, obj, **partial_params):
        self.obj = obj
        self.partial_params = partial_params

    def __getattr__(self, name):
        return functools.partial(getattr(self.obj, name),
                                 **self.partial_params)


@pytest.fixture
def client():
    from django.test.client import Client

    class _Client(Client):
        def login(self, user=None,
                  backend="django.contrib.auth.backends.ModelBackend",
                  **credentials):
            if user is None:
                return super(_Client, self).login(**credentials)

            with mock.patch('django.contrib.auth.authenticate') as authenticate:
                user.backend = backend
                authenticate.return_value = user
                return super(_Client, self).login(**credentials)

        @property
        def json(self):
            return PartialMethodCaller(obj=self, content_type='application/json;charset="utf-8"')

    return _Client()


@pytest.fixture
def outbox():
    from django.core import mail

    return mail.outbox


# App Fixture


@pytest.fixture
def conferences():
    # Create conference with closed date
    today = datetime.datetime.today()
    day_before_yesterday = today - datetime.timedelta(days=2)
    yesterday = today - datetime.timedelta(days=1)
    closed_status = ConferenceStatus._CLOSED_CFP[0]
    past = factories.create_conference(name="Past",
                                       start_date=day_before_yesterday,
                                       end_date=yesterday,
                                       status=closed_status)

    # Create conference with future date
    today = datetime.datetime.today()
    tomo = today + datetime.timedelta(days=1)
    open_status = ConferenceStatus._ACCEPTING_CFP[0]
    future = factories.create_conference(name="Future",
                                         start_date=today,
                                         end_date=tomo,
                                         status=open_status)
    return {'past': past, 'future': future}


@pytest.fixture
def create_user():
    username, password = "username", "password"
    user = factories.create_user(username=username,
                                 email="username@example.com",
                                 password=password)
    user.set_password(password)
    user.is_active = True
    user.save()
    return {'username': username, 'password': password, 'user': user}


@pytest.fixture
def create_superuser(create_user):
    user = create_user['user']
    user.is_staff = True
    user.is_superuser = True
    user.save()
    create_user['user'] = user
    return create_user


@pytest.fixture
def login(create_user, client):
    username, password = create_user['username'], create_user['password']
    client.login(username=username, password=password)
    return client, create_user['user']


@pytest.fixture
def create_reviewer(create_user, conferences):
    user = create_user['user']
    conference = conferences['future']
    conference_reviewer = ConferenceProposalReviewer.objects.create(
        conference=conference,
        reviewer=user)
    for section in conference.proposal_sections.all():
        ProposalSectionReviewer.objects.create(
            conference_reviewer=conference_reviewer,
            proposal_section=section)
    return user


@pytest.fixture
def create_proposal(conferences, create_user):
    conference, user = conferences['future'], create_user['user']
    section = conference.proposal_sections.all()[0]
    proposal_type = conference.proposal_types.all()[0]
    proposal = factories.create_proposal(conference=conference,
                                         proposal_section=section,
                                         proposal_type=proposal_type,
                                         author=user)
    return proposal
