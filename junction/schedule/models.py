from django.db import models

from junction.base.models import AuditModel
from junction.proposals.models import Proposal
from junction.conferences.models import Conference, Room


class ScheduleItem(AuditModel):
    room = models.ForeignKey(Room, null=True)
    # if a session is not present, venue can be null Ex: break
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    alt_name = models.CharField(max_length=100, blank=True)
    session = models.ForeignKey(Proposal, null=True)

    conference = models.ForeignKey(Conference)

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        return self.alt_name or self.session.title
