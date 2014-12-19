from django.contrib.auth.models import User
from django.db import models

from conferences.models import Conference
from custom_utils.constants import PROPOSAL_STATUS_DRAFT, \
     PROPOSAL_REVIEW_STATUS_YET_TO_BE_REVIEWED, \
    PROPOSAL_USER_VOTE_ROLE_PUBLIC, PROPOSAL_COMMENT_VISIBILITY_PUBLIC, \
    PROPOSAL_COMMENT_VISIBILITY_OPTIONS, PROPOSAL_USER_VOTE_ROLES, \
    PROPOSAL_STATUS_LIST, PROPOSAL_REVIEW_STATUS_LIST
from custom_utils.models import AuditModel, TimeAuditModel


class ProposalSection(AuditModel):
    """ List of Proposal Sections """
    name = models.CharField(max_length=255, verbose_name="Proposal Section Name")
    description = models.TextField(default="")
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return self.name


class ProposalType(AuditModel):
    """ List of Proposal Types """
    name = models.CharField(max_length=255, verbose_name="Proposal Type Name")
    description = models.TextField(default="")
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return self.name


class ConferenceProposalSection(AuditModel):
    """ List of proposals sections allowed for a specific conferences """
    conference = models.ForeignKey(Conference)
    proposal_section = models.ForeignKey(ProposalSection, verbose_name="Proposal Section")
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return "{}[{}]".format(self.proposal_section, self.conference)

    class Meta:
        unique_together = ("conference", "proposal_section")


class ConferenceProposalType(AuditModel):
    """ List of proposals types allowed for a specific conferences """
    conference = models.ForeignKey(Conference)
    proposal_type = models.ForeignKey(ProposalType, verbose_name="Proposal Type")
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return "{}[{}]".format(self.proposal_type, self.conference)

    class Meta:
        unique_together = ("conference", "proposal_type")


class Proposal(TimeAuditModel):
    """ The proposals master """
    conference = models.ForeignKey(Conference)
    proposal_section = models.ForeignKey(ProposalSection, verbose_name="Proposal Section")
    proposal_type = models.ForeignKey(ProposalType, verbose_name="Proposal Type")
    author = models.ForeignKey(User, verbose_name="Primary Speaker")
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    target_audienance = models.TextField(default="")
    prerequisites = models.TextField(default="")
    content_urls = models.TextField(default="")
    speaker_info = models.TextField(default="")
    speaker_links = models.TextField(default="")
    status = models.CharField(max_length=255, choices=PROPOSAL_STATUS_LIST, default=PROPOSAL_STATUS_DRAFT)
    review_status = models.CharField(max_length=255, choices=PROPOSAL_REVIEW_STATUS_LIST, default=PROPOSAL_REVIEW_STATUS_YET_TO_BE_REVIEWED, verbose_name="Review Status")
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    def __unicode__(self):
        return self.title


class ProposalVote(TimeAuditModel):
    """ User vote for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    voter = models.ForeignKey(User)
    role = models.CharField(max_length=255, choices=PROPOSAL_USER_VOTE_ROLES, default=PROPOSAL_USER_VOTE_ROLE_PUBLIC)
    up_vote = models.BooleanField(default=True)

    def __unicode__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal)

    class Meta:
        unique_together = ("proposal", "voter")


class ProposalComment(TimeAuditModel):
    """ User comments for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    commenter = models.ForeignKey(User)
    visibility = models.CharField(max_length=255, choices=PROPOSAL_COMMENT_VISIBILITY_OPTIONS, default=PROPOSAL_COMMENT_VISIBILITY_PUBLIC)
    comment = models.TextField()
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    def __unicode__(self):
        return "[{}] {}".format(self.commenter.get_full_name(), self.proposal)


class ProposalCommentVote(TimeAuditModel):
    """ User vote for a specific proposal's comment """
    proposal_comment = models.ForeignKey(ProposalComment)
    voter = models.ForeignKey(User)
    up_vote = models.BooleanField(default=True)

    def __unicode__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal_comment)

    class Meta:
        unique_together = ("proposal_comment", "voter")

