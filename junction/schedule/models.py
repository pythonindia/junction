# -*- coding: utf-8 -*-

from django.db import models
from six import python_2_unicode_compatible
from rest_framework.reverse import reverse

from junction.base.constants import ProposalReviewStatus
from junction.base.models import AuditModel
from junction.conferences.models import Conference, Room
from junction.proposals.models import Proposal


@python_2_unicode_compatible
class ScheduleItemType(AuditModel):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ScheduleItem(AuditModel):
    INTROUDCTION = "Introduction"
    TALK = "Talk"
    LUNCH = "Lunch"
    BREAK = "Break"
    WORKSHOP = "Workshop"
    POSTER = "Poster"
    OPEN_SPACE = "Open Space"
    LIGHTNING_TALK = "Lightning Talk"
    SCHEDULE_ITEM_TYPE = (
        (TALK, "Talk"),
        (LUNCH, "Lunch"),
        (BREAK, "Break"),
        (WORKSHOP, "Workshop"),
        (POSTER, "Poster"),
        (OPEN_SPACE, "Open Space"),
        (INTROUDCTION, "Introduction"),
        (LIGHTNING_TALK, "Lightning Talk"),
    )
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    # if a session is not present, venue can be null Ex: break
    event_date = models.DateField(db_index=True)
    start_time = models.TimeField(db_index=True)
    end_time = models.TimeField()
    alt_name = models.CharField(max_length=255, blank=True)
    alt_description = models.TextField(blank=True)
    limit_choices = {"review_status": ProposalReviewStatus.SELECTED}
    session = models.ForeignKey(
        Proposal,
        null=True,
        blank=True,
        limit_choices_to=limit_choices,
        on_delete=models.SET_NULL,
    )
    type = models.CharField(max_length=20, choices=SCHEDULE_ITEM_TYPE, default=TALK)

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __unicode__(self):
        return "{} - {} on {} from {} to {} in {}".format(
            self.conference,
            self.name,
            self.event_date,
            self.start_time,
            self.end_time,
            self.room,
        )

    @property
    def name(self):
        return self.alt_name or self.session.title

    class Meta:
        index_together = [("event_date", "start_time")]

    def to_response(self, request):
        """method will return dict which can be passed to response
        """
        data = {
            "id": self.id,
            "room_id": getattr(self.room, "id", None),
            "event_date": self.event_date.strftime("%Y-%m-%d"),
            "start_time": self.start_time.strftime("%H:%M:%S"),
            "end_time": self.end_time.strftime("%H:%M:%S"),
            "name": self.name,
            "type": self.type,
            "conference": reverse(
                "conference-detail", kwargs={"pk": self.conference_id}, request=request
            ),
        }
        if self.session:
            session = self.session
            author = "{} {}".format(session.author.first_name, session.author.last_name)
            data["session"] = {
                "id": session.id,
                "title": session.title,
                "section": session.proposal_section.name,
                "author": author,
                "description": session.description,
                "target_audience": session.target_audience,
                "prerequisites": session.prerequisites,
                "content_urls": session.content_urls,
                "speaker_links": session.speaker_links,
                "speaker_info": session.speaker_info,
            }
        else:
            data["session"] = {"description": self.alt_description}
        return data
