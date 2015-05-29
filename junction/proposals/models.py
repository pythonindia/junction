# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
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


@python_2_unicode_compatible
class ProposalSection(AuditModel):

    """ List of Proposal Sections"""
    name = models.CharField(max_length=255, verbose_name="Proposal Section Name")
    description = models.TextField(default="")
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    conferences = models.ManyToManyField(to=Conference, related_name='proposal_sections')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProposalSectionReviewer(AuditModel):

    """ List of Proposal Section Reviewers"""
    conference_reviewer = models.ForeignKey('conferences.ConferenceProposalReviewer',
                                            verbose_name="Conference Proposal Reviewers")
    proposal_section = models.ForeignKey(ProposalSection, verbose_name="Proposal Section")
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return "{}:[{}]".format(self.conference_reviewer, self.proposal_section)


@python_2_unicode_compatible
class ProposalType(AuditModel):

    """ List of Proposal Types """
    name = models.CharField(max_length=255, verbose_name="Proposal Type Name")
    description = models.TextField(default="")
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    conferences = models.ManyToManyField(to=Conference, related_name='proposal_types')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
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
    prerequisites = models.TextField(blank=True, default="")
    content_urls = models.TextField(blank=True, default="")
    speaker_info = models.TextField(blank=True, default="")
    speaker_links = models.TextField(blank=True, default="")
    status = models.PositiveSmallIntegerField(
        choices=PROPOSAL_STATUS_LIST, default=1)
    review_status = models.PositiveSmallIntegerField(
        choices=PROPOSAL_REVIEW_STATUS_LIST, default=1, verbose_name="Review Status")
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('proposal-detail', args=[self.conference.slug, self.slug])

    def get_update_url(self):
        return reverse('proposal-update', args=[self.conference.slug, self.slug])

    def get_review_url(self):
        return reverse('proposal-review', args=[self.conference.slug, self.slug])

    def get_delete_url(self):
        return reverse('proposal-delete', args=[self.conference.slug, self.slug])

    def get_up_vote_url(self):
        return reverse('proposal-vote-up', args=[self.conference.slug, self.slug])

    def get_down_vote_url(self):
        return reverse('proposal-vote-down', args=[self.conference.slug, self.slug])

    def get_comments_count(self):
        """ Show only the public comment count """
        return ProposalComment.objects.filter(proposal=self, deleted=False, private=False).count()

    def get_reviews_comments_count(self):
        """ Show only the public comment count """
        return ProposalComment.objects.filter(proposal=self, deleted=False, private=True).count()

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


@python_2_unicode_compatible
class ProposalVote(TimeAuditModel):

    """ User vote for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    voter = models.ForeignKey(User)
    role = models.PositiveSmallIntegerField(
        choices=PROPOSAL_USER_VOTE_ROLES, default=1)
    up_vote = models.BooleanField(default=True)

    def __str__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal)

    class Meta:
        unique_together = ("proposal", "voter")


class ProposalCommentQuerySet(models.QuerySet):
    def get_public_comments(self):
        return self.filter(private=False, reviewer=False)

    def get_reviewers_comments(self):
        return self.filter(private=True)

    def get_reviewers_only_comments(self):
        return self.filter(reviewer=True)


class ProposalCommentManager(models.Manager):
    def get_queryset(self):
        return ProposalCommentQuerySet(self.model, using=self._db)

    def get_public_comments(self):
        return self.get_queryset().get_public_comments()

    def get_reviewers_comments(self):
        return self.get_queryset().get_reviewers_comments()

    def get_reviewers_only_comments(self):
        return self.get_queryset().get_reviewers_only_comments()


@python_2_unicode_compatible
class ProposalComment(TimeAuditModel):

    """ User comments for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    commenter = models.ForeignKey(User)
    private = models.BooleanField(default=False, verbose_name="Is Private?")
    reviewer = models.BooleanField(default=False, verbose_name="Is Reviewer?")
    comment = models.TextField()
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    objects = ProposalCommentManager()

    def __str__(self):
        return "[{} by {}] {}".format(self.comment,
                                      self.commenter.get_full_name(),
                                      self.proposal)

    def get_up_vote_url(self):
        return reverse('proposal-comment-up-vote', args=[self.proposal.conference.slug, self.proposal.slug, self.id])

    def get_down_vote_url(self):
        return reverse('proposal-comment-down-vote', args=[self.proposal.conference.slug, self.proposal.slug, self.id])

    def get_votes_count(self):
        up_vote_count = ProposalCommentVote.objects.filter(proposal_comment=self, up_vote=True).count()
        down_vote_count = ProposalCommentVote.objects.filter(proposal_comment=self, up_vote=False).count()
        return up_vote_count - down_vote_count


@python_2_unicode_compatible
class ProposalCommentVote(TimeAuditModel):

    """ User vote for a specific proposal's comment """
    proposal_comment = models.ForeignKey(ProposalComment)
    voter = models.ForeignKey(User)
    up_vote = models.BooleanField(default=True)

    def __str__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal_comment)

    class Meta:
        unique_together = ("proposal_comment", "voter")
