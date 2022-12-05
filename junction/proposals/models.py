# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.template.defaultfilters import slugify
from six import python_2_unicode_compatible
from django_extensions.db.fields import AutoSlugField
from hashids import Hashids
from rest_framework.reverse import reverse as rf_reverse
from simple_history.models import HistoricalRecords

from junction.base.constants import (
    ProposalCommentType,
    ProposalReviewStatus,
    ProposalReviewVote,
    ProposalStatus,
    ProposalTargetAudience,
    ProposalUserVoteRole,
    PSRVotePhase,
)
from junction.base.models import AuditModel, TimeAuditModel
from junction.conferences.models import Conference, ConferenceProposalReviewer


@python_2_unicode_compatible
class ProposalSection(AuditModel):

    """ List of Proposal Sections"""

    name = models.CharField(max_length=255, verbose_name="Proposal Section Name")
    description = models.TextField(default="", blank=True)
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    conferences = models.ManyToManyField(
        to=Conference, related_name="proposal_sections"
    )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ProposalSectionReviewer(AuditModel):

    """ List of Proposal Section Reviewers"""

    conference_reviewer = models.ForeignKey(
        "conferences.ConferenceProposalReviewer",
        verbose_name="Conference Proposal Reviewers",
        on_delete=models.CASCADE,
    )
    proposal_section = models.ForeignKey(
        ProposalSection, verbose_name="Proposal Section", on_delete=models.CASCADE
    )
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __str__(self):
        return "{}:[{}]".format(self.conference_reviewer, self.proposal_section)


@python_2_unicode_compatible
class ProposalType(AuditModel):

    """ List of Proposal Types """

    name = models.CharField(max_length=255, verbose_name="Proposal Type Name")
    description = models.TextField(default="", blank=True)
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    conferences = models.ManyToManyField(to=Conference, related_name="proposal_types")
    start_date = models.DateField(default=datetime.now, verbose_name="Start Date")
    end_date = models.DateField(default=datetime.now, verbose_name="End Date")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Proposal(TimeAuditModel):

    """ The proposals master """

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    proposal_section = models.ForeignKey(
        ProposalSection, verbose_name="Proposal Section", on_delete=models.CASCADE
    )
    proposal_type = models.ForeignKey(
        ProposalType, verbose_name="Proposal Type", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, verbose_name="Primary Speaker", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    slug = AutoSlugField(max_length=255, populate_from=("title",))
    description = models.TextField(default="")
    target_audience = models.PositiveSmallIntegerField(
        choices=ProposalTargetAudience.CHOICES,
        default=ProposalTargetAudience.BEGINNER,
        verbose_name="Target Audience",
    )
    video_url = models.URLField(
        blank=True, default="", help_text="Short 1-2 min video describing your talk",
    )
    prerequisites = models.TextField(blank=True, default="")
    content_urls = models.TextField(blank=True, default="")
    private_content_urls = models.BooleanField(
        default=False,
        help_text="Check it if you want to make your content URLs private",
    )
    speaker_info = models.TextField(blank=True, default="")
    speaker_links = models.TextField(blank=True, default="")
    is_first_time_speaker = models.BooleanField(blank=True, default=False)
    status = models.PositiveSmallIntegerField(
        choices=ProposalStatus.CHOICES, default=ProposalStatus.DRAFT
    )
    review_status = models.PositiveSmallIntegerField(
        choices=ProposalReviewStatus.CHOICES,
        default=ProposalReviewStatus.YET_TO_BE_REVIEWED,
        verbose_name="Review Status",
    )
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
        return reverse(
            "proposal-detail",
            args=[self.conference.slug, self.get_slug(), self.get_hashid()],
        )

    def get_update_url(self):
        return reverse("proposal-update", args=[self.conference.slug, self.slug])

    def get_review_url(self):
        return reverse("proposal-review", args=[self.conference.slug, self.slug])

    def get_vote_url(self):
        return reverse("proposal-reviewer-vote", args=[self.conference.slug, self.slug])

    def get_secondary_vote_url(self):
        return reverse(
            "proposal-reviewer-secondary-vote", args=[self.conference.slug, self.slug]
        )

    def get_delete_url(self):
        return reverse("proposal-delete", args=[self.conference.slug, self.slug])

    def get_up_vote_url(self):
        return reverse("proposal-vote-up", args=[self.conference.slug, self.slug])

    def get_down_vote_url(self):
        return reverse("proposal-vote-down", args=[self.conference.slug, self.slug])

    def get_remove_vote_url(self):
        return reverse("proposal-vote-remove", args=[self.conference.slug, self.slug])

    def get_comments_count(self):
        """ Show only public comments count """
        return ProposalComment.objects.filter(
            proposal=self, deleted=False, private=False, vote=False, reviewer=False
        ).count()

    def get_reviews_comments_count(self):
        """ Show only private comments count """
        return ProposalComment.objects.filter(
            proposal=self, deleted=False, private=True, vote=False
        ).count()

    def get_reviewer_comments_count(self, reviewer):
        """ Number of private comments by a reviewer """
        return ProposalComment.objects.filter(
            proposal=self, deleted=False, private=True, commenter=reviewer, vote=False
        ).count()

    def get_votes_count(self):
        """ Show only the public comment count """
        votes = (
            ProposalVote.objects.filter(proposal=self)
            .values("up_vote")
            .annotate(counts=models.Count("up_vote"))
        )
        votes = {item["up_vote"]: item["counts"] for item in votes}
        up_vote_count = votes.get(True, 0)
        down_vote_count = votes.get(False, 0)
        return up_vote_count - down_vote_count

    def get_reviewer_votes_count(self):
        """ Show sum of reviewer vote value. """
        return ProposalSectionReviewerVote.objects.filter(proposal=self).count()

    def get_reviewer_votes_count_by_value(self, vote_value):
        """ Show sum of reviewer votes for given vote value. """
        return ProposalSectionReviewerVote.objects.filter(
            proposal=self, vote_value__vote_value=vote_value
        ).count()

    def get_reviewer_votes_sum(self):
        votes = ProposalSectionReviewerVote.objects.filter(proposal=self,)
        sum_of_votes = sum((v.vote_value.vote_value for v in votes))
        return sum_of_votes

    def get_reviewer_vote_value(self, reviewer):
        try:
            vote = ProposalSectionReviewerVote.objects.get(
                proposal=self, voter__conference_reviewer__reviewer=reviewer,
            )
            return vote.vote_value.vote_value
        except ProposalSectionReviewerVote.DoesNotExist:
            return 0

    def get_reviewers_count(self):
        """ Count of reviewers for given proposal section """
        return ProposalSectionReviewer.objects.filter(
            proposal_section=self.proposal_section
        ).count()

    def has_negative_votes(self):
        """ Show sum of reviewer votes for given vote value. """
        return (
            ProposalSectionReviewerVote.objects.filter(
                proposal=self, vote_value__vote_value=ProposalReviewVote.NOT_ALLOWED,
            ).count()
            > 0
        )

    def to_response(self, request):
        """method will return dict which can be passed to response
        """
        author = "{} {}".format(self.author.first_name, self.author.last_name)
        data = {
            "id": self.id,
            "author": author,
            "title": self.title,
            "description": self.description,
            "target_audience": dict(ProposalTargetAudience.CHOICES)[
                self.target_audience
            ],
            "status": dict(ProposalStatus.CHOICES)[self.status],
            "review_status": dict(ProposalReviewStatus.CHOICES)[self.review_status],
            "proposal_type": self.proposal_type.name,
            "proposal_section": self.proposal_section.name,
            "votes_count": self.get_votes_count(),
            "speaker_info": self.speaker_info,
            "speaker_links": self.speaker_links,
            "content_urls": self.content_urls,
            "private_content_urls": self.private_content_urls,
            "conference": rf_reverse(
                "conference-detail", kwargs={"pk": self.conference_id}, request=request
            ),
        }
        return data

    class Meta:
        unique_together = ("conference", "slug")


@python_2_unicode_compatible
class ProposalVote(TimeAuditModel):

    """ User vote for a specific proposal """

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(
        choices=ProposalUserVoteRole.CHOICES, default=ProposalUserVoteRole.PUBLIC
    )
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
        ordering = ("-vote_value",)


@python_2_unicode_compatible
class ProposalSectionReviewerVote(TimeAuditModel):

    """ Reviewer vote for a specific proposal """

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    voter = models.ForeignKey(ProposalSectionReviewer, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(
        choices=ProposalUserVoteRole.CHOICES, default=ProposalUserVoteRole.REVIEWER
    )
    vote_value = models.ForeignKey(
        ProposalSectionReviewerVoteValue, on_delete=models.CASCADE
    )
    phase = models.PositiveSmallIntegerField(
        choices=PSRVotePhase.CHOICES, default=PSRVotePhase.PRIMARY
    )

    history = HistoricalRecords()

    def __str__(self):
        return "[{}] {}".format(self.vote_value, self.proposal)

    class Meta:
        verbose_name = "ProposalSectionReviewerVote"


# FIXME: Need to move private, reviewer, vote to type
@python_2_unicode_compatible
class ProposalComment(TimeAuditModel):

    """ User comments for a specific proposal """

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False, verbose_name="Is Private?")
    reviewer = models.BooleanField(default=False, verbose_name="Is Reviewer?")
    vote = models.BooleanField(default=False, verbose_name="What is the reason?")
    comment = models.TextField()
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")
    comment_type = models.PositiveSmallIntegerField(
        choices=ProposalCommentType.CHOICES, default=ProposalCommentType.GENERAL
    )
    objects = ProposalCommentQuerySet.as_manager()
    is_spam = models.BooleanField(default=False, blank=True)
    marked_as_spam_by = models.ForeignKey(
        User,
        related_name="marked_as_spam_by",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ("created_at",)
        index_together = [["is_spam", "marked_as_spam_by"], ["commenter", "is_spam"]]

    def __str__(self):
        return "[{} by {}] {}".format(
            self.comment, self.commenter.get_full_name(), self.proposal
        )

    def get_up_vote_url(self):
        return reverse(
            "proposal-comment-up-vote",
            args=[self.proposal.conference.slug, self.proposal.slug, self.id],
        )

    def get_down_vote_url(self):
        return reverse(
            "proposal-comment-down-vote",
            args=[self.proposal.conference.slug, self.proposal.slug, self.id],
        )

    def get_mark_spam_url(self):
        return reverse(
            "comment_mark_spam",
            args=[self.proposal.conference.slug, self.proposal.slug, self.id],
        )

    def get_unmark_spam_url(self):
        return reverse(
            "comment_unmark_spam",
            args=[self.proposal.conference.slug, self.proposal.slug, self.id],
        )

    def get_votes_count(self):
        up_vote_count = ProposalCommentVote.objects.filter(
            proposal_comment=self, up_vote=True
        ).count()
        down_vote_count = ProposalCommentVote.objects.filter(
            proposal_comment=self, up_vote=False
        ).count()
        return up_vote_count - down_vote_count

    def get_reviewer_nick(self):
        reviewer = ConferenceProposalReviewer.objects.get(
            conference_id=self.proposal.conference_id, reviewer_id=self.commenter_id
        )
        return reviewer.nick

    def get_comment_type(self):
        if self.deleted:
            return "Deleted"
        elif self.vote:
            return "Vote"
        elif self.reviewer:
            return "Reviewer Only"
        elif self.private:
            return "Review"
        else:
            return "Public"


@python_2_unicode_compatible
class ProposalCommentVote(TimeAuditModel):

    """ User vote for a specific proposal's comment """

    proposal_comment = models.ForeignKey(ProposalComment, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    up_vote = models.BooleanField(default=True)

    def __str__(self):
        return "[{}] {}".format("1" if self.up_vote else "-1", self.proposal_comment)

    class Meta:
        unique_together = ("proposal_comment", "voter")
