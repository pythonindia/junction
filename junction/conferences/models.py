# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.template.loader import render_to_string
from django.template.context import RequestContext, Context

from junction.custom_utils.constants import CONFERENCE_STATUS_LIST
from junction.custom_utils.models import AuditModel
from junction.custom_utils.emailer import EmailEngine

def _get_conference_moderator_emails(conference):
    return [(cm.moderator.email)
            for cm in ConferenceModerator.objects.filter(conference=conference)]

class Conference(AuditModel):

    """ Conference/Event master """
    name = models.CharField(max_length=255, verbose_name="Conference Name")
    slug = AutoSlugField(max_length=255, unique=True, populate_from=('name',))
    description = models.TextField(default="")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    status = models.PositiveSmallIntegerField(
        choices=CONFERENCE_STATUS_LIST, verbose_name="Current Status")
    deleted = models.BooleanField(default=False, verbose_name="Is Deleted?")

    def __unicode__(self):
        return self.name
    
    def save(self, **kwargs):
        ''' Save function overrided inorder to send an email to all 
            moderators when ever the conference data is changed '''
        if self.id is None:
            super(Conference, self).save(**kwargs)
        else:
            html_page = render_to_string("emails/conference_data_change_email.html",
                                        {
                                         'name': self.name,
                                         'description':self.description,
                                         'start_date':self.start_date,
                                         'end_date':self.end_date,
                                         'status':dict(CONFERENCE_STATUS_LIST)[self.status],
                                         'modified_user':self.modified_by.get_full_name(),
                                         'modified_date':self.modified_at.strftime("%d %b %Y"),
                                         'class':'Conference',
                                        }
                                        )
            subject = "Notification for data modification of the conference - "+self.name 
            to_list = _get_conference_moderator_emails(self)

            if to_list:
                email_engine = EmailEngine()
                email_engine.send_email(to_list,html_page,subject)
            
            super(Conference, self).save(**kwargs)
        
    

class ConferenceModerator(AuditModel):

    """ List of Conference Moderators/Administrators  """
    conference = models.ForeignKey(Conference)
    moderator = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return "{}[{}]".format(self.moderator.get_full_name(), self.conference)
    
    def save(self, **kwargs):
        ''' Save function overrided inorder to send an email to all 
            moderators when ever the conference data is changed '''
        super(ConferenceModerator, self).save(**kwargs)
        
        html_page = render_to_string("emails/conference_data_change_email.html",
                                    {
                                     'conference_name':self.conference.name,
                                     'moderator': self.moderator.get_full_name(),
                                     'added_date':self.created_at.strftime("%d %b %Y"),
                                     'class':'ConferenceModerator',
                                    }
                                    )
        subject = "New Moderator added to the conference - "+self.conference.name 
        to_list = _get_conference_moderator_emails(self.conference)
        
        if to_list:
            email_engine = EmailEngine()
            email_engine.send_email(to_list,html_page,subject)
            

class ConferenceProposalReviewer(AuditModel):

    """ List of global proposal reviewers """
    conference = models.ForeignKey(Conference)
    reviewer = models.ForeignKey(User)
    active = models.BooleanField(default=True, verbose_name="Is Active?")

    def __unicode__(self):
        return "{}[{}]".format(self.reviewer.get_full_name(), self.conference)

    class Meta:
        unique_together = ("conference", "reviewer")

    def save(self, **kwargs):
        ''' Save function overrided inorder to send an email to all 
            moderators when ever the conference data is changed '''
        super(ConferenceProposalReviewer, self).save(**kwargs)
        
        html_page = render_to_string("emails/conference_data_change_email.html",
                                    {
                                     'conference_name':self.conference.name,
                                     'reviewer': self.reviewer.get_full_name(),
                                     'added_date':self.created_at.strftime("%d %b %Y"),
                                     'class':'ConferenceProposalReviewer',
                                    }
                                    )
        subject = "New Proposal Reviewer added to the conference - "+self.conference.name 
        to_list = _get_conference_moderator_emails(self.conference)
        if to_list:
            email_engine = EmailEngine()
            email_engine.send_email(to_list,html_page,subject)
