from django.db import models

from junction.base.models import AuditModel
from junction.proposals.models import Proposal
from junction.conferences.models import Conference, Room


class ScheduleItem(AuditModel):
    TALK = 'TALK'
    LUNCH = 'LUNCH'
    BREAK = 'BREAK'
    SCHEDULE_ITEM_TYPE = ((TALK, 'Talk'),
                          (LUNCH, 'Lunch'),
                          (BREAK, 'Break'))
    room = models.ForeignKey(Room, null=True)
    # if a session is not present, venue can be null Ex: break
    event_date = models.DateField(db_index=True)
    start_time = models.TimeField(db_index=True)
    end_time = models.TimeField()
    alt_name = models.CharField(max_length=100, blank=True)
    session = models.ForeignKey(Proposal, null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_ITEM_TYPE,
                            default=TALK)

    conference = models.ForeignKey(Conference)

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        return self.alt_name or self.session.title

    class Meta:
        index_together = [
            ('event_date', 'start_time')
        ]
