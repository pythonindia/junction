# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models

from junction.base.models import AuditModel


class Ticket(AuditModel):
    """
    Conference ticket details
    """

    order_no = models.CharField(max_length=255)
    order_cost = models.FloatField()
    ticket_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    city = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    others = models.JSONField()

    def __str__(self):
        return self.name, self.email, self.ticket_no
