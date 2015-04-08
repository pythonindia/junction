# -*- coding: utf-8 -*-
# Standard Library
import threading
import datetime

# Third Party Stuff
import factory
from factory import fuzzy

# Junction Stuff
from junction.base.constants import CONFERENCE_STATUS_LIST


class Factory(factory.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True

    _SEQUENCE = 1
    _SEQUENCE_LOCK = threading.Lock()

    @classmethod
    def _setup_next_sequence(cls):
        with cls._SEQUENCE_LOCK:
            cls._SEQUENCE += 1 
        return cls._SEQUENCE


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

    #fd = fuzzy.FuzzyDate(datetime.date.today(), datetime.date(2017,1,1))
    name = factory.Sequence(lambda n: "conference{}".format(n))
    #slug = factory.LazyAttribute(lambda obj: slugify)
    # description = 
    start_date = fuzzy.FuzzyDate(datetime.date.today(), datetime.date(2017,1,1)).fuzz()
    end_date = start_date + datetime.timedelta(3)
    # logo
    status = factory.Iterator(dict(CONFERENCE_STATUS_LIST).keys())
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
                self.conferences.add(group)


class ProposalSectionReviewerFactory(Factory):
    class Meta:
        model = "proposals.ProposalSectionReviewer"
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
    # title
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

def create_conference(**kwargs):
    """ Create a conference """
    return ConferenceFactory.create(**kwargs)

def create_user(**kwargs):
    "Create an user along with her dependencies"
    return UserFactory.create(**kwargs)

def create_proposal(**kwargs):
    return ProposalFactory.create(**kwargs)
