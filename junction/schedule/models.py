# -*- coding: utf-8 -*-

from django.db import models

from junction.base.models import AuditModel
from junction.base.constants import ProposalReviewStatus
from junction.proposals.models import Proposal
from junction.conferences.models import Conference, Room

from rest_framework.reverse import reverse


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

    def to_response(self, request):
        """method will return dict which can be passed to response
        """
        data = {'id': self.id,
                'room_id': getattr(self.room, 'id', None),
                'event_date': self.event_date.strftime("%Y-%m-%d"),
                'start_time': self.start_time.strftime("%H:%M:%S"),
                'end_time': self.end_time.strftime("%H:%M:%S"),
                'name': self.name,
                'conference': reverse("conference-detail",
                                      kwargs={'pk': self.conference_id},
                                      request=request)}
        if self.session:
            session = self.session
            author = u"{} {}".format(session.author.first_name,
                                     session.author.last_name)
            data['session'] = {'id': session.id,
                               'title': session.title,
                               'section': session.proposal_section.name,
                               'author': author,
                               'description': session.description,
                               'target_audience': session.target_audience,
                               'prerequisites': session.prerequisites,
                               'content_urls': session.content_urls,
                               'speaker_links': session.speaker_links,
                               'speaker_info': session.speaker_info}
        return data
