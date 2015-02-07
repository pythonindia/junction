# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django_extensions.db.fields import AutoSlugField
from junction.base.constants import CONFERENCE_STATUS_LIST
from junction.base.models import AuditModel

from slugify import slugify
from uuid_upload_path import upload_to


class Conference(AuditModel):

    """ Conference/Event master """
    name = models.CharField(max_length=255, verbose_name="Conference Name")
    slug = AutoSlugField(max_length=255, unique=True, populate_from=('name',), editable=True)
    description = models.TextField(default="")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    logo = models.ImageField(blank=True, null=True, upload_to=upload_to)
    status = models.PositiveSmallIntegerField(
        choices=CONFERENCE_STATUS_LIST, verbose_name="Current Status")
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    class Meta:
        verbose_name = _('Conference')
        verbose_name_plural = _('Conferences')
        ordering = ('-start_date', 'name',)
        get_latest_by = 'start_date'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("conference-detail", kwargs={'conference_slug': self.slug})

    def clean(self):
        if self.end_date < self.start_date:
            msg = _("End date should be greater than start date.")
            raise ValidationError({'end_date': msg})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Conference, self).save(*args, **kwargs)


class ConferenceModerator(AuditModel):

    """ List of Conference Moderators/Administrators  """
    conference = models.ForeignKey(Conference, related_name='moderators')
    moderator = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    class Meta:
        unique_together = ("conference", "moderator")
        verbose_name = 'moderator'
        verbose_name_plural = 'moderators'

    def __unicode__(self):
        return "{}[{}]".format(self.moderator.get_full_name(), self.conference)


class EmailNotificationSetting(AuditModel):

    """ List of email notifications for proposal reviewers """
    conference = models.ForeignKey(Conference, related_name='email_notification')
    proposal_section = models.ForeignKey('proposals.ProposalSection')
    proposal_type = models.ForeignKey('proposals.ProposalType')

    class Meta:
        verbose_name = 'email notification'
        verbose_name_plural = 'email notifications'

    def __unicode__(self):
        return "{}[{}:{}]".format(self.conference, self.proposal_section,
                                  self.proposal_type)


# class ConferenceProposalReviewerManager(models.Manager):
#     """ Custom manager class for ConferenceProposalReviewer """

#     def create(self, conference, reviewer, active):
#         cpr = self.create(conference, reviewer, active)
#         [cpr.notifications.add(e) for e in
#          EmailNotificationSetting.objects.filter(conference=conference)]
#         return cpr


class ConferenceProposalReviewer(AuditModel):

    """ List of global proposal reviewers """
    conference = models.ForeignKey(Conference, related_name='proposal_reviewers')
    reviewer = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    notifications = models.ManyToManyField(EmailNotificationSetting, blank=True,
                                           null=True)

    # objects = ConferenceProposalReviewerManager()

    class Meta:
        verbose_name = 'proposals reviewer'
        verbose_name_plural = 'proposals reviewers'
        unique_together = ("conference", "reviewer")

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         super(ConferenceProposalReviewer, self).save(*args, **kwargs)
    #         [self.notifications.add(e) for e in
    #          EmailNotificationSetting.objects.filter()]
    #     super(ConferenceProposalReviewer, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{}[{}]".format(self.reviewer.get_full_name(), self.conference)
