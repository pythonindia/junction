# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib.auth.models import User
from django.db import models


class TimeAuditModel(models.Model):
    """To track when the record was created and last modified
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Last Modified At")

    class Meta:
        abstract = True


class UserAuditModel(models.Model):
    """ To track who created and last modified the record
    """
    created_by = models.ForeignKey(User, related_name='created_%(class)s_set',
                                   null=True, blank=True, verbose_name="Created By")
    modified_by = models.ForeignKey(User, related_name='updated_%(class)s_set',
                                    null=True, blank=True, verbose_name="Modified By")

    class Meta:
        abstract = True


class AuditModel(TimeAuditModel, UserAuditModel):

    class Meta:
        abstract = True
