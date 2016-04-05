# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django_extensions.db.fields import AutoSlugField
from simple_history.models import HistoricalRecords
from slugify import slugify
from uuid_upload_path import upload_to

# Junction Stuff
from junction.base.utils import get_date_diff_display
from junction.base.constants import ConferenceSettingConstants, ConferenceStatus
from junction.base.models import AuditModel


@python_2_unicode_compatible
class Conference(AuditModel):

    """ Conference/Event master """
    name = models.CharField(max_length=255, verbose_name="Conference Name")
    slug = AutoSlugField(max_length=255, unique=True, populate_from=('name',),
                         editable=True)
    description = models.TextField(default="")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    logo = models.ImageField(blank=True, null=True, upload_to=upload_to)
    status = models.PositiveSmallIntegerField(
        choices=ConferenceStatus.CHOICES, verbose_name="Current Status")
    venue = models.ForeignKey('ConferenceVenue', null=True, blank=True)

    twitter_id = models.CharField(max_length=100, blank=True, null=True, default='',
                                  help_text=_('Used in social share widgets.'))
    hashtags = models.CharField(max_length=100, blank=True, null=True, default='',
                                help_text=_("Used in social sharing, use commas to separate to tags, no '#' required."))

    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    class Meta:
        verbose_name = _('Conference')
        verbose_name_plural = _('Conferences')
        ordering = ('-start_date', 'name',)
        get_latest_by = 'start_date'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("conference-detail", kwargs={'conference_slug':
                                                    self.slug})

    def duration_display(self):
        return get_date_diff_display(self.start_date, self.end_date)

    def clean(self):
        if self.end_date < self.start_date:
            msg = _("End date should be greater than start date.")
            raise ValidationError({'end_date': msg})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.pk:
            super(Conference, self).save(*args, **kwargs)
            public_voting = ConferenceSettingConstants.ALLOW_PUBLIC_VOTING_ON_PROPOSALS
            ConferenceSetting.objects.create(name=public_voting['name'],
                                             value=public_voting['value'],
                                             description=public_voting['description'],
                                             conference=self)
            display_propsals = ConferenceSettingConstants.DISPLAY_PROPOSALS_IN_PUBLIC
            ConferenceSetting.objects.create(name=display_propsals['name'],
                                             value=display_propsals['value'],
                                             description=display_propsals['description'],
                                             conference=self)
            allow_plus_zero_vote = ConferenceSettingConstants.ALLOW_PLUS_ZERO_REVIEWER_VOTE
            ConferenceSetting.objects.create(
                name=allow_plus_zero_vote['name'],
                value=allow_plus_zero_vote['value'],
                description=allow_plus_zero_vote['description'],
                conference=self)
            return
        super(Conference, self).save(*args, **kwargs)

    def is_accepting_proposals(self):
        """Check if any one of the proposal section is accepting proposal.
        """
        if (self.status == ConferenceStatus.CLOSED_CFP or
                self.status == ConferenceStatus.SCHEDULE_PUBLISHED):
            return False
        return self.proposal_types.filter(end_date__gt=now()).exists()


@python_2_unicode_compatible
class ConferenceModerator(AuditModel):

    """ List of Conference Moderators/Administrators  """
    conference = models.ForeignKey(Conference, related_name='moderators')
    moderator = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    class Meta:
        unique_together = ("conference", "moderator")
        verbose_name = 'moderator'
        verbose_name_plural = 'moderators'

    def __str__(self):
        return "{}[{}]".format(self.moderator.get_full_name(), self.conference)


@python_2_unicode_compatible
class ConferenceProposalReviewer(AuditModel):

    """ List of global proposal reviewers """
    conference = models.ForeignKey(Conference,
                                   related_name='proposal_reviewers')
    reviewer = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")
    nick = models.CharField(max_length=255, verbose_name="Nick Name",
                            default="Reviewer")
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'proposals reviewer'
        verbose_name_plural = 'proposals reviewers'
        unique_together = ("conference", "reviewer")

    def __str__(self):
        return "{} - {}".format(self.conference, self.reviewer.username)


@python_2_unicode_compatible
class ConferenceVenue(AuditModel):
    name = models.CharField(max_length=100)

    address = models.TextField()

    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitudes = models.DecimalField(max_digits=19, decimal_places=16)

    def __str__(self):
        return self.name


class Room(AuditModel):
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(ConferenceVenue)

    note = models.CharField(max_length=255)

    def __str__(self):
        return "{}, {}".format(self.name, self.venue)


@python_2_unicode_compatible
class ConferenceSetting(AuditModel):
    conference = models.ForeignKey(Conference)
    name = models.CharField(max_length=100, db_index=True)
    value = models.BooleanField(default=False)
    description = models.CharField(max_length=255)

    def __str__(self):
        return "{}: {}".format(self.name, self.value)
