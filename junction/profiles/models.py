from django.db import models
from django.contrib.auth.models import User


class Profiles(models.Model):
	''' 
	It stores the City/Phone Details of the User.
	'''
	user=models.OneToOneField(User)
	city=models.CharField(max_length=100, blank=False, null=False)
	contact_no = models.CharField(max_length=10, blank=False, null=False)

	created = models.DateTimeField("Created", null=True, auto_now_add=True)
	modified = models.DateTimeField("Last Modified", null=True, auto_now=True)

	def __unicode__(self):
		return self.user.username
