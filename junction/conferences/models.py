from django.contrib.auth.models import User
from django.db import models

from custom_utils.constants import CONFERENCE_STATUS_LIST
from custom_utils.models import AuditModel


class Conference(AuditModel):
    """ Conference/Event master """
    name = models.CharField(max_length=255, verbose_name="Conference Name")
    description = models.TextField(default="")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    status = models.PositiveSmallIntegerField(choices=CONFERENCE_STATUS_LIST, verbose_name="Current Status")
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    def __unicode__(self):
        return self.name


class ConferenceModerator(AuditModel):
    """ List of Conference Moderators/Administrators  """
    conference = models.ForeignKey(Conference)
    moderator = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return "{}[{}]".format(self.moderator.get_full_name(), self.conference)


class ConferenceProposalReviewer(AuditModel):
    """ List of global proposal reviewers """
    conference = models.ForeignKey(Conference)
    reviewer = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return "{}[{}]".format(self.reviewer.get_full_name(), self.conference)

    class Meta:
        unique_together = ("conference", "reviewer")

