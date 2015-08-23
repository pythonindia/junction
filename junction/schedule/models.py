from django.db import models

from junction.base.models import AuditModel
from junction.base.constants import ProposalReviewStatus
from junction.proposals.models import Proposal
from junction.conferences.models import Conference, Room


class ScheduleItem(AuditModel):
    TALK = 'TALK'
    LUNCH = 'LUNCH'
    BREAK = 'BREAK'
    WORKSHOP = 'WORKSHOP'
    POSTER = 'POSTER'
    OPEN_SPACE = "OPEN_SPACE"
    SCHEDULE_ITEM_TYPE = ((TALK, 'Talk'),
                          (LUNCH, 'Lunch'),
                          (BREAK, 'Break'),
                          (WORKSHOP, 'Workshop'),
                          (POSTER, 'Poster'),
                          (OPEN_SPACE, 'Open Space'))
    room = models.ForeignKey(Room, null=True)
    # if a session is not present, venue can be null Ex: break
    event_date = models.DateField(db_index=True)
    start_time = models.TimeField(db_index=True)
    end_time = models.TimeField()
    alt_name = models.CharField(max_length=100, blank=True)
    session = models.ForeignKey(
        Proposal,
        limit_choices_to={'review_status': ProposalReviewStatus.SELECTED},
        null=True)
    type = models.CharField(max_length=20, choices=SCHEDULE_ITEM_TYPE,
                            default=TALK)

    conference = models.ForeignKey(Conference)

    def __unicode__(self):
        return u"{} - {} on {} from {} to {} in {}".format(
            self.conference, self.name, self.event_date, self.start_time,
            self.end_time, self.room)

    @property
    def name(self):
        return self.alt_name or self.session.title

    class Meta:
        index_together = [
            ('event_date', 'start_time')
        ]
