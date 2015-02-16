# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django_extensions.db.fields import AutoSlugField

# Junction Stuff
from junction.base.constants import (
    PROPOSAL_REVIEW_STATUS_LIST,
    PROPOSAL_STATUS_LIST,
    PROPOSAL_TARGET_AUDIENCES,
    PROPOSAL_USER_VOTE_ROLES
)
from junction.base.models import AuditModel, TimeAuditModel
from junction.conferences.models import Conference


class ProposalSection(AuditModel):

    """ List of Proposal Sections"""
    name = models.CharField(max_length=255, verbose_name="Proposal Section Name")
    description = models.TextField(default="")
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    conferences = models.ManyToManyField(to=Conference, related_name='proposal_sections')

    def __unicode__(self):
        return self.name


class ProposalSectionReviewer(AuditModel):

    """ List of Proposal Section Reviewers"""
    conference_reviewer = models.ForeignKey('conferences.ConferenceProposalReviewer',
                                            verbose_name="Conference Proposal Reviewers")
    proposal_section = models.ForeignKey(ProposalSection, verbose_name="Proposal Section")
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return "{}:[{}]".format(self.conference_reviewer, self.proposal_section)


class ProposalType(AuditModel):

    """ List of Proposal Types """
    name = models.CharField(max_length=255, verbose_name="Proposal Type Name")
    description = models.TextField(default="")
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    conferences = models.ManyToManyField(to=Conference, related_name='proposal_types')

    def __unicode__(self):
        return self.name


class Proposal(TimeAuditModel):

    """ The proposals master """
    conference = models.ForeignKey(Conference)
    proposal_section = models.ForeignKey(ProposalSection, verbose_name="Proposal Section")
    proposal_type = models.ForeignKey(ProposalType, verbose_name="Proposal Type")
    author = models.ForeignKey(User, verbose_name="Primary Speaker")
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from=('title',))
    description = models.TextField(default="")
    target_audience = models.PositiveSmallIntegerField(
        choices=PROPOSAL_TARGET_AUDIENCES, default=1, verbose_name="Target Audience")
    prerequisites = models.TextField(default="")
    content_urls = models.TextField(default="")
    speaker_info = models.TextField(default="")
    speaker_links = models.TextField(default="")
    status = models.PositiveSmallIntegerField(
        choices=PROPOSAL_STATUS_LIST, default=1)
    review_status = models.PositiveSmallIntegerField(
        choices=PROPOSAL_REVIEW_STATUS_LIST, default=1, verbose_name="Review Status")
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('proposal-detail', args=[self.conference.slug, self.slug])

    def get_update_url(self):
        return reverse('proposal-update', args=[self.conference.slug, self.slug])

    def get_delete_url(self):
        return reverse('proposal-delete', args=[self.conference.slug, self.slug])

    def get_up_vote_url(self):
        return reverse('proposal-vote-up', args=[self.conference.slug, self.slug])

    def get_down_vote_url(self):
        return reverse('proposal-vote-down', args=[self.conference.slug, self.slug])

    def get_comments_count(self):
        """ Show only the public comment count """
        return ProposalComment.objects.filter(proposal=self, deleted=False, private=False).count()

    def get_votes_count(self):
        """ Show only the public comment count """
        up_vote_count = ProposalVote.objects.filter(proposal=self, up_vote=True).count()
        down_vote_count = ProposalVote.objects.filter(proposal=self, up_vote=False).count()
        return up_vote_count - down_vote_count

    def status_text(self):
        """ Text representation of status values """
        for value, text in PROPOSAL_STATUS_LIST:
            if self.status == value:
                return text

    class Meta:
        unique_together = ("conference", "slug")


class ProposalVote(TimeAuditModel):

    """ User vote for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    voter = models.ForeignKey(User)
    role = models.PositiveSmallIntegerField(
        choices=PROPOSAL_USER_VOTE_ROLES, default=1)
    up_vote = models.BooleanField(default=True)

    def __unicode__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal)

    class Meta:
        unique_together = ("proposal", "voter")


class ProposalComment(TimeAuditModel):

    """ User comments for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    commenter = models.ForeignKey(User)
    private = models.BooleanField(default=False, verbose_name="Is Private?")
    comment = models.TextField()
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    def __unicode__(self):
        return "[{}] {}".format(self.commenter.get_full_name(), self.proposal)

    def get_up_vote_url(self):
        return reverse('proposal-comment-up-vote', args=[self.proposal.conference.slug, self.proposal.slug, self.id])

    def get_down_vote_url(self):
        return reverse('proposal-comment-down-vote', args=[self.proposal.conference.slug, self.proposal.slug, self.id])

    def get_votes_count(self):
        up_vote_count = ProposalCommentVote.objects.filter(proposal_comment=self, up_vote=True).count()
        down_vote_count = ProposalCommentVote.objects.filter(proposal_comment=self, up_vote=False).count()
        return up_vote_count - down_vote_count


class ProposalCommentVote(TimeAuditModel):

    """ User vote for a specific proposal's comment """
    proposal_comment = models.ForeignKey(ProposalComment)
    voter = models.ForeignKey(User)
    up_vote = models.BooleanField(default=True)

    def __unicode__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal_comment)

    class Meta:
        unique_together = ("proposal_comment", "voter")
