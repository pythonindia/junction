# Conference Application Choice Fields
CONFERENCE_STATUS_ACCEPTING_CFP = "Accepting Call for Proposals"
CONFERENCE_STATUS_CLOSED_CFP = "Closed for Proposals"
CONFERENCE_STATUS_ACCEPTING_VOTES = "Accepting Votes"
CONFERENCE_STATUS_SCHEDULE_PUBLISHED = "Schedule Published"

CONFERENCE_STATUS_LIST = (("0", CONFERENCE_STATUS_ACCEPTING_CFP),
                          ("1", CONFERENCE_STATUS_CLOSED_CFP),
                          ("2", CONFERENCE_STATUS_ACCEPTING_VOTES),
                          ("3", CONFERENCE_STATUS_SCHEDULE_PUBLISHED),
                          )

# Proposal Application Choice Fields
PROPOSAL_STATUS_DRAFT = "Draft"
PROPOSAL_STATUS_PUBLIC = "Public"
PROPOSAL_STATUS_CANCELLED = "Cancelled"

PROPOSAL_STATUS_LIST = (("0", PROPOSAL_STATUS_DRAFT),
                        ("1", PROPOSAL_STATUS_PUBLIC),
                        ("2", PROPOSAL_STATUS_CANCELLED),
                        )

PROPOSAL_REVIEW_STATUS_YET_TO_BE_REVIEWED = "Yet to be reviewed"
PROPOSAL_REVIEW_STATUS_SELECTED = "Selected"
PROPOSAL_REVIEW_STATUS_REJECTED = "Rejected"
PROPOSAL_REVIEW_STATUS_ON_HOLD = " On hold"
PROPOSAL_REVIEW_STATUS_WAIT_LISTED = "Wait-listed"

PROPOSAL_REVIEW_STATUS_LIST = (("0", PROPOSAL_REVIEW_STATUS_YET_TO_BE_REVIEWED),
                               ("1", PROPOSAL_REVIEW_STATUS_SELECTED),
                               ("2", PROPOSAL_REVIEW_STATUS_REJECTED),
                               ("3", PROPOSAL_REVIEW_STATUS_ON_HOLD),
                               ("4", PROPOSAL_REVIEW_STATUS_WAIT_LISTED),
                               )

PROPOSAL_USER_VOTE_ROLE_PUBLIC = "Public"
PROPOSAL_USER_VOTE_ROLE_REVIEWER = "Reviewer"

PROPOSAL_USER_VOTE_ROLES = (("0", PROPOSAL_USER_VOTE_ROLE_PUBLIC),
                            ("1", PROPOSAL_USER_VOTE_ROLE_REVIEWER),
                            )

PROPOSAL_COMMENT_VISIBILITY_PUBLIC = "Public"
PROPOSAL_COMMENT_VISIBILITY_PRIVATE = "Private"

PROPOSAL_COMMENT_VISIBILITY_OPTIONS = (("0", PROPOSAL_COMMENT_VISIBILITY_PUBLIC),
                                       ("1", PROPOSAL_COMMENT_VISIBILITY_PRIVATE),
                                       )
