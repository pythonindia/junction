# -*- coding: utf-8 -*-

# Standard Library
import datetime
from datetime import timedelta
import uuid

# Third Party Stuff
import factory
from factory import fuzzy

# Junction Stuff
from junction.base.constants import ConferenceStatus


class Factory(factory.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True


class UserFactory(Factory):
    class Meta:
        model = "auth.User"
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.LazyAttribute(lambda obj: '%s@email.com' % obj.username)
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password('123123'))


class ConferenceFactory(Factory):
    class Meta:
        model = "conferences.Conference"
        strategy = factory.CREATE_STRATEGY

    # fd = fuzzy.FuzzyDate(datetime.date.today(), datetime.date(2017,1,1))
    name = factory.Sequence(lambda n: "conference{}".format(n))
    # slug = factory.LazyAttribute(lambda obj: slugify)
    # description =
    start_date = fuzzy.FuzzyDate(datetime.date.today(),
                                 datetime.date(datetime.date.today().year + 1, 1, 1)).fuzz()
    end_date = start_date + datetime.timedelta(3)
    # logo
    status = factory.Iterator(list(dict(ConferenceStatus.CHOICES).keys()))
    # deleted


class ProposalSectionFactory(Factory):
    class Meta:
        model = "proposals.ProposalSection"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "proposalsection{}".format(n))

    @factory.post_generation
    def conferences(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of conferences were passed in, use them
            for conference in extracted:
                self.conferences.add(conference)


class ProposalSectionReviewerFactory(Factory):
    class Meta:
        model = "proposals.ProposalSectionReviewer"
        strategy = factory.CREATE_STRATEGY


class ProposalSectionReviewerVoteValueFactory(Factory):
    class Meta:
        model = "proposals.ProposalSectionReviewerVoteValue"
        strategy = factory.CREATE_STRATEGY


class ProposalTypeFactory(Factory):
    class Meta:
        model = "proposals.ProposalType"
        strategy = factory.CREATE_STRATEGY


class ProposalVoteFactory(Factory):
    class Meta:
        model = "proposals.ProposalVote"
        strategy = factory.CREATE_STRATEGY


class ProposalCommentFactory(Factory):
    class Meta:
        model = "proposals.ProposalComment"
        strategy = factory.CREATE_STRATEGY


class ProposalCommentVoteFactory(Factory):
    class Meta:
        model = "proposals.ProposalCommentVote"
        strategy = factory.CREATE_STRATEGY


class ProposalFactory(Factory):
    class Meta:
        model = 'proposals.Proposal'
        strategy = factory.CREATE_STRATEGY

    conference = factory.SubFactory("tests.factories.ConferenceFactory")
    proposal_section = factory.SubFactory("tests.factories.ProposalSectionFactory")
    proposal_type = factory.SubFactory('tests.factories.ProposalTypeFactory')
    author = factory.SubFactory("tests.factories.UserFactory")
    title = factory.LazyAttribute(lambda x: "Propsoal %s" % x)
    # slug
    # description
    # target_audience
    # choices
    # prerequisites
    # content_urls
    # speaker_info
    # speaker_links
    # status
    # choices
    # review_status
    # choices
    # deleted


class DeviceFactory(Factory):
    class Meta:
        model = "devices.Device"
        strategy = factory.CREATE_STRATEGY


class ScheduleItemFactory(Factory):
    class Meta:
        model = "schedule.ScheduleItem"
        strategy = factory.CREATE_STRATEGY

    event_date = fuzzy.FuzzyDate(datetime.date.today(),
                                 datetime.date.today() + timedelta(days=90)).fuzz()
    start_time = fuzzy.FuzzyChoice(['9:30.750000', ]).fuzz()
    end_time = fuzzy.FuzzyChoice(['10:15.750000', ]).fuzz()
    conference = factory.SubFactory("tests.factories.ConferenceFactory")
    session = factory.SubFactory("tests.factories.ProposalFactory")


class ScheduleItemTypeFactory(Factory):
    class Meta:
        model = "schedule.ScheduleItemType"
        strategy = factory.CREATE_STRATEGY
        django_get_or_create = ('title',)


class TextFeedbackQuestionFactory(Factory):
    class Meta:
        model = 'feedback.TextFeedbackQuestion'
        strategy = factory.CREATE_STRATEGY

    schedule_item_type = factory.SubFactory(
        'tests.factories.ScheduleItemTypeFactory')
    conference = factory.SubFactory("tests.factories.ConferenceFactory")


class ChoiceFeedbackQuestionFactory(Factory):
    class Meta:
        model = 'feedback.ChoiceFeedbackQuestion'
        strategy = factory.CREATE_STRATEGY

    schedule_item_type = factory.SubFactory(
        'tests.factories.ScheduleItemTypeFactory')
    conference = factory.SubFactory("tests.factories.ConferenceFactory")


class ChoiceFeedbackQuestionValueFactory(Factory):
    class Meta:
        model = 'feedback.ChoiceFeedbackQuestionValue'
        strategy = factory.CREATE_STRATEGY
    question = factory.SubFactory(
        "tests.factories.ChoiceFeedbackQuestionFactory")
    title = factory.Sequence(lambda n: "title{}".format(n))
    value = factory.Sequence(lambda n: n)


def create_conference(**kwargs):
    """ Create a conference """
    ProposalSectionReviewerVoteValueFactory.create(vote_value=1,
                                                   description="Good")
    ProposalSectionReviewerVoteValueFactory.create(vote_value=2,
                                                   description="Good")
    conference = ConferenceFactory.create(**kwargs)
    start_date = kwargs.pop('start_date', None)
    end_date = kwargs.pop('end_date', None)
    if start_date and end_date:
        workshop = ProposalTypeFactory.create(name="Workshop",
                                              start_date=start_date,
                                              end_date=end_date)
        conference.proposal_types.add(workshop)
        talks = ProposalTypeFactory.create(name="Talks",
                                           start_date=start_date,
                                           end_date=end_date)
        conference.proposal_types.add(talks)
        conference.save()

    section = ProposalSectionFactory.create()
    conference.proposal_sections.add(section)
    section = ProposalSectionFactory.create()
    conference.proposal_sections.add(section)
    conference.save()
    return conference


def create_user(**kwargs):
    "Create an user along with her dependencies"
    user = UserFactory.create(**kwargs)
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
        user.is_active = True
        user.save()
    return user


def create_proposal(**kwargs):
    return ProposalFactory.create(**kwargs)


def create_schedule_item_type(**kwargs):
    return ScheduleItemFactory.create(**kwargs)


def create_text_feedback_question(**kwargs):
    return TextFeedbackQuestionFactory(**kwargs)


def create_choice_feedback_question(**kwargs):
    question = ChoiceFeedbackQuestionFactory(**kwargs)
    ChoiceFeedbackQuestionValueFactory.create(
        question=question, title="Bad", value=0)
    ChoiceFeedbackQuestionValueFactory.create(
        question=question, title="Ok", value=1)
    ChoiceFeedbackQuestionValueFactory.create(
        question=question, title="Awesome", value=2)


def create_feedback_questions(schedule_item_types,
                              num_text_questions,
                              num_choice_questions):
    conference = create_conference()
    item_types = []
    for item_type in schedule_item_types:
        item = ScheduleItemTypeFactory.create(title=item_type)
        item_types.append(item)

    choices = []
    for _ in range(num_choice_questions):
        for item_type in item_types:
            obj = ChoiceFeedbackQuestionFactory.create(
                schedule_item_type=item_type,
                conference=conference, is_required=True)
            ChoiceFeedbackQuestionValueFactory.create(
                question=obj)
            ChoiceFeedbackQuestionValueFactory.create(
                question=obj)
            ChoiceFeedbackQuestionValueFactory.create(
                question=obj)
            choices.append(obj)

    text = []
    for _ in range(num_text_questions):
        for item_type in item_types:
            obj = TextFeedbackQuestionFactory.create(
                schedule_item_type=item_type,
                conference=conference, is_required=True)
            text.append(obj)

    d = {'conference': conference, 'text': text, 'choices': choices}
    return d


def create_device(**kwargs):
    uuid1 = uuid.uuid1()
    kwargs['uuid'] = uuid1
    kwargs['verification_code'] = '2345'
    return DeviceFactory.create(**kwargs)


def create_schedule_items(**kwargs):
    d = []
    for item_type in kwargs['item_types']:
        ScheduleItemTypeFactory.create(title=item_type)
        d.append(ScheduleItemFactory.create(type=item_type,
                                            conference=kwargs['conference']))
    return d
