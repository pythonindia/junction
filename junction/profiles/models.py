from django.contrib.auth.models import User
from django.db import models

from junction.base.models import AuditModel


class Profile(AuditModel):
    '''
    It stores the City/Phone Details of the User.
    '''
    user = models.OneToOneField(User)
    city = models.CharField(max_length=100, blank=True, null=True)
    contact_no = models.CharField(max_length=15, blank=True, null=True)

    def __unicode__(self):
        return self.user.username
