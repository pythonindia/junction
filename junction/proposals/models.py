# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
from datetime import datetime

# Third Party Stuff
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.fields import AutoSlugField
from hashids import Hashids
from simple_history.models import HistoricalRecords

# Junction Stuff
from junction.base.constants import ProposalReviewStatus, ProposalStatus, ProposalTargetAudience, ProposalUserVoteRole
from junction.base.models import AuditModel, TimeAuditModel
from junction.conferences.models import Conference, ConferenceProposalReviewer


@python_2_unicode_compatible
class ProposalSection(AuditModel):

    """ List of Proposal Sections"""
    name = models.CharField(max_length=255, verbose_name="Proposal Section Name")
    description = models.TextField(default="", blank=True)
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
    description = models.TextField(default="", blank=True)
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    conferences = models.ManyToManyField(to=Conference, related_name='proposal_types')
    start_date = models.DateField(default=datetime.now, verbose_name="Start Date")
    end_date = models.DateField(default=datetime.now, verbose_name="End Date")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Proposal(TimeAuditModel):

    """ The proposals master """
    conference = models.ForeignKey(Conference)
    proposal_section = models.ForeignKey(ProposalSection,
                                         verbose_name="Proposal Section")
    proposal_type = models.ForeignKey(ProposalType,
                                      verbose_name="Proposal Type")
    author = models.ForeignKey(User, verbose_name="Primary Speaker")
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from=('title',))
    description = models.TextField(default="")
    target_audience = models.PositiveSmallIntegerField(
        choices=ProposalTargetAudience.CHOICES,
        default=ProposalTargetAudience.BEGINNER,
        verbose_name="Target Audience")
    prerequisites = models.TextField(blank=True, default="")
    content_urls = models.TextField(blank=True, default="")
    speaker_info = models.TextField(blank=True, default="")
    speaker_links = models.TextField(blank=True, default="")
    status = models.PositiveSmallIntegerField(
        choices=ProposalStatus.CHOICES, default=ProposalStatus.DRAFT)
    review_status = models.PositiveSmallIntegerField(
        choices=ProposalReviewStatus.CHOICES,
        default=ProposalReviewStatus.YET_TO_BE_REVIEWED,
        verbose_name="Review Status")
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")
    history = HistoricalRecords()

    def __str__(self):
        return "{}, {}".format(self.title, self.proposal_type)

    def is_public(self):
        # TODO: Fix with proper enum
        return self.status == 2

    def get_slug(self):
        return slugify(self.title)

    def get_hashid(self):
        hashids = Hashids(min_length=5)
        return hashids.encode(self.id)

    def get_absolute_url(self):
        return reverse('proposal-detail',
                       args=[self.conference.slug, self.get_slug(), self.get_hashid()])

    def get_update_url(self):
        return reverse('proposal-update',
                       args=[self.conference.slug, self.slug])

    def get_review_url(self):
        return reverse('proposal-review',
                       args=[self.conference.slug, self.slug])

    def get_vote_url(self):
        return reverse('proposal-reviewer-vote',
                       args=[self.conference.slug, self.slug])

    def get_delete_url(self):
        return reverse('proposal-delete',
                       args=[self.conference.slug, self.slug])

    def get_up_vote_url(self):
        return reverse('proposal-vote-up',
                       args=[self.conference.slug, self.slug])

    def get_down_vote_url(self):
        return reverse('proposal-vote-down',
                       args=[self.conference.slug, self.slug])

    def get_remove_vote_url(self):
        return reverse('proposal-vote-remove',
                       args=[self.conference.slug, self.slug])

    def get_comments_count(self):
        """ Show only public comments count """
        return ProposalComment.objects.filter(proposal=self,
                                              deleted=False,
                                              private=False,
                                              vote=False,
                                              reviewer=False).count()

    def get_reviews_comments_count(self):
        """ Show only private comments count """
        return ProposalComment.objects.filter(proposal=self,
                                              deleted=False,
                                              private=True,
                                              vote=False).count()

    def get_reviewer_comments_count(self, reviewer):
        """ Number of private comments by a reviewer """
        return ProposalComment.objects.filter(
            proposal=self, deleted=False, private=True,
            commenter=reviewer, vote=False).count()

    def get_votes_count(self):
        """ Show only the public comment count """
        votes = ProposalVote.objects.filter(
            proposal=self
        ).values('up_vote').annotate(counts=models.Count('up_vote'))
        votes = {item['up_vote']: item['counts'] for item in votes}
        up_vote_count = votes.get(True, 0)
        down_vote_count = votes.get(False, 0)
        return up_vote_count - down_vote_count

    def get_reviewer_votes_count(self):
        """ Show sum of reviewer vote value. """
        return ProposalSectionReviewerVote.objects.filter(
            proposal=self
        ).count()

    def get_reviewer_votes_count_by_value(self, vote_value):
        """ Show sum of reviewer votes for given vote value. """
        return ProposalSectionReviewerVote.objects.filter(
            proposal=self, vote_value=vote_value
        ).count()

    def get_reviewer_votes_sum(self):
        votes = ProposalSectionReviewerVote.objects.filter(
            proposal=self,
        )
        sum_of_votes = sum((v.vote_value.vote_value for v in votes))
        return sum_of_votes

    def get_reviewers_count(self):
        """ Count of reviewers for given proposal section """
        return ProposalSectionReviewer.objects.filter(
            proposal_section=self.proposal_section
        ).count()

    class Meta:
        unique_together = ("conference", "slug")


@python_2_unicode_compatible
class ProposalVote(TimeAuditModel):

    """ User vote for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    voter = models.ForeignKey(User)
    role = models.PositiveSmallIntegerField(
        choices=ProposalUserVoteRole.CHOICES, default=ProposalUserVoteRole.PUBLIC)
    up_vote = models.BooleanField(default=True)

    def __str__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal)

    class Meta:
        unique_together = ("proposal", "voter")


class ProposalCommentQuerySet(models.QuerySet):
    def get_public_comments(self):
        return self.filter(private=False, reviewer=False, vote=False)

    def get_reviewers_comments(self):
        return self.filter(private=True, vote=False)

    def get_reviewers_only_comments(self):
        return self.filter(reviewer=True, vote=False)


@python_2_unicode_compatible
class ProposalSectionReviewerVoteValue(AuditModel):
    """ Proposal reviewer vote choices. """
    vote_value = models.SmallIntegerField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return "{} ({})".format(self.description, self.vote_value)

    class Meta:
        ordering = ('-vote_value',)


@python_2_unicode_compatible
class ProposalSectionReviewerVote(TimeAuditModel):

    """ Reviewer vote for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    voter = models.ForeignKey(ProposalSectionReviewer)
    role = models.PositiveSmallIntegerField(
        choices=ProposalUserVoteRole.CHOICES, default=ProposalUserVoteRole.REVIEWER)
    vote_value = models.ForeignKey(ProposalSectionReviewerVoteValue)
    history = HistoricalRecords()

    def __str__(self):
        return "[{}] {}".format(self.vote_value, self.proposal)

    class Meta:
        unique_together = ("proposal", "voter")
        verbose_name = 'ProposalSectionReviewerVote'


@python_2_unicode_compatible
class ProposalComment(TimeAuditModel):

    """ User comments for a specific proposal """
    proposal = models.ForeignKey(Proposal)
    commenter = models.ForeignKey(User)
    private = models.BooleanField(default=False, verbose_name="Is Private?")
    reviewer = models.BooleanField(default=False, verbose_name="Is Reviewer?")
    vote = models.BooleanField(default=False, verbose_name="What is the reason?")
    comment = models.TextField()
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    objects = ProposalCommentQuerySet.as_manager()

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

    def get_reviewer_nick(self):
        reviewer = ConferenceProposalReviewer.objects.get(conference_id=self.proposal.conference_id,
                                                          reviewer_id=self.commenter_id)
        return reviewer.nick

    def get_comment_type(self):
        if self.deleted:
            return 'Deleted'
        elif self.vote:
            return 'Vote'
        elif self.reviewer:
            return 'Reviewer Only'
        elif self.private:
            return 'Review'
        else:
            return 'Public'


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
