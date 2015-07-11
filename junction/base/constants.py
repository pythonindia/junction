# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

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


# Proposal Application Choice Fields
PROPOSAL_STATUS_DRAFT = 1
PROPOSAL_STATUS_PUBLIC = 2
PROPOSAL_STATUS_CANCELLED = 3

PROPOSAL_STATUS_LIST = ((PROPOSAL_STATUS_PUBLIC, "Public"),
                        (PROPOSAL_STATUS_DRAFT, "Draft"),
                        (PROPOSAL_STATUS_CANCELLED, "Cancelled"),
                        )

PROPOSAL_REVIEW_STATUS_YET_TO_BE_REVIEWED = 1
PROPOSAL_REVIEW_STATUS_SELECTED = 2
PROPOSAL_REVIEW_STATUS_REJECTED = 3
PROPOSAL_REVIEW_STATUS_ON_HOLD = 4
PROPOSAL_REVIEW_STATUS_WAIT_LISTED = 5

PROPOSAL_REVIEW_STATUS_LIST = ((PROPOSAL_REVIEW_STATUS_YET_TO_BE_REVIEWED, "Yet to be reviewed"),
                               (PROPOSAL_REVIEW_STATUS_SELECTED, "Selected"),
                               (PROPOSAL_REVIEW_STATUS_REJECTED, "Rejected"),
                               (PROPOSAL_REVIEW_STATUS_ON_HOLD, "On hold"),
                               (PROPOSAL_REVIEW_STATUS_WAIT_LISTED, "Wait-listed"),
                               )

PROPOSAL_TARGET_AUDIENCE_BEGINNER = "Beginner"
PROPOSAL_TARGET_AUDIENCE_INTERMEDIATE = "Intermediate"
PROPOSAL_TARGET_AUDIENCE_ADVANCED = "Advanced"

PROPOSAL_TARGET_AUDIENCES = ((1, PROPOSAL_TARGET_AUDIENCE_BEGINNER),
                             (2, PROPOSAL_TARGET_AUDIENCE_INTERMEDIATE),
                             (3, PROPOSAL_TARGET_AUDIENCE_ADVANCED),
                             )

PROPOSAL_USER_VOTE_ROLE_PUBLIC = "Public"
PROPOSAL_USER_VOTE_ROLE_REVIEWER = "Reviewer"

PROPOSAL_USER_VOTE_ROLES = ((1, PROPOSAL_USER_VOTE_ROLE_PUBLIC),
                            (2, PROPOSAL_USER_VOTE_ROLE_REVIEWER),
                            )

PROPOSAL_REVIEW_VOTE_MUST_HAVE = "Must have"
PROPOSAL_REVIEW_VOTE_GOOD = "Good"
PROPOSAL_REVIEW_VOTE_NOT_BAD = "Not Bad"
PROPOSAL_REVIEW_VOTE_NOT_ALLOWED = "Shouldn't be allowed"

PROPOSAL_REVIEW_VOTES_LIST = ((2, PROPOSAL_REVIEW_VOTE_MUST_HAVE),
                              (1, PROPOSAL_REVIEW_VOTE_GOOD),
                              (0, PROPOSAL_REVIEW_VOTE_NOT_BAD),
                              (-1, PROPOSAL_REVIEW_VOTE_NOT_ALLOWED),
                              )

REVIEWER_HAS_COMMENTED = 'Yes'
REVIEWER_HAS_NOT_COMMENTED = 'No'
PROPOSAL_REVIEWER_COMMENT_CHOICES = (('True', REVIEWER_HAS_COMMENTED),
                                     ('False', REVIEWER_HAS_NOT_COMMENTED),
                                     )
