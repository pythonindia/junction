from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    '''
    It stores the City/Phone Details of the User.
    '''
    user = models.OneToOneField(User)
    city = models.CharField(max_length=100, blank=False, null=False)
    contact_no = models.CharField(max_length=10, blank=False, null=False)

    def __unicode__(self):
        return self.user.username
