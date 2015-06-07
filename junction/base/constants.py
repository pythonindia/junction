# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Conference Application Choice Fields
CONFERENCE_STATUS_ACCEPTING_CFP = "Accepting Proposals"
CONFERENCE_STATUS_CLOSED_CFP = "Proposal submission closed"
CONFERENCE_STATUS_ACCEPTING_VOTES = "Accepting Votes"
CONFERENCE_STATUS_SCHEDULE_PUBLISHED = "Schedule Published"

CONFERENCE_STATUS_LIST = ((1, CONFERENCE_STATUS_ACCEPTING_CFP),
                          (2, CONFERENCE_STATUS_CLOSED_CFP),
                          (3, CONFERENCE_STATUS_ACCEPTING_VOTES),
                          (4, CONFERENCE_STATUS_SCHEDULE_PUBLISHED),
                          )

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
