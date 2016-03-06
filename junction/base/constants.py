# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import inspect


def _user_attributes(cls):
    defaults = dir(type(str('defaults'), (object,), {}))  # gives all inbuilt attrs
    return [
        item[0] for item in inspect.getmembers(cls) if item[0] not in defaults]


def choices(cls):
    """
    Decorator to set `CHOICES` and other attributes
    """
    _choices = []
    for attr in _user_attributes(cls):
        val = getattr(cls, attr)
        setattr(cls, attr[1:], val[0])
        _choices.append((val[0], val[1]))
    setattr(cls, 'CHOICES', tuple(_choices))
    return cls


@choices
class ConferenceStatus:
    _ACCEPTING_CFP = [1, "Accepting Proposals"]
    _CLOSED_CFP = [2, "Proposal submission closed"]
    _ACCEPTING_VOTES = [3, "Accepting Votes"]
    _SCHEDULE_PUBLISHED = [4, "Schedule Published"]


@choices
class ProposalStatus:
    _DRAFT = [1, "Draft"]
    _PUBLIC = [2, "Public"]
    _CANCELLED = [3, "Cancelled"]


@choices
class ProposalReviewStatus:
    _YET_TO_BE_REVIEWED = [1, "Yet to be reviewed"]
    _SELECTED = [2, "Selected"]
    _REJECTED = [3, "Rejected"]
    _ON_HOLD = [4, "On hold"]
    _WAIT_LISTED = [5, "Wait-listed"]


@choices
class ProposalTargetAudience:
    _BEGINNER = [1, "Beginner"]
    _INTERMEDIATE = [2, "Intermediate"]
    _ADVANCED = [3, "Advanced"]


@choices
class ProposalUserVoteRole:
    _PUBLIC = [1, "Public"]
    _REVIEWER = [2, "Reviewer"]


@choices
class ProposalReviewVote:
    _MUST_HAVE = [2, "Must have"]
    _GOOD = [1, "Good"]
    _NOT_BAD = [0, "Not Bad"]
    _NOT_ALLOWED = [-1, "Shouldn't be allowed"]


# FIXME: `ProposalReviewerComment` should be Boolean
@choices
class ProposalReviewerComment:
    _COMMENTED = ['True', 'Yes']
    _NOT_COMMENTED = ['False', 'No']


@choices
class ProposalVotesFilter:
    _NO_VOTES = [0, "No votes"]
    _MIN_ONE_VOTE = [1, "Minimum 1 vote"]
    _SORT = [2, "Sort by vote value"]


class ConferenceSettingConstants:
    ALLOW_PUBLIC_VOTING_ON_PROPOSALS = {
        "name": "allow_public_voting_on_proposals",
        "value": True,
        "description": "Allow public to vote on proposals"}

    DISPLAY_PROPOSALS_IN_PUBLIC = {"name": "display_proposals_in_public",
                                   "value": True,
                                   "description": "Display proposals in public"}

    ALLOW_PLUS_ZERO_REVIEWER_VOTE = {"name": "allow_plus_zero_reviewer_vote",
                                     "value": True,
                                     "description": "Allow +0 vote in reviewer votes"}
