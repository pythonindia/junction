# -*- coding: utf-8 -*-

# Standard Library
import datetime

# Third Party Stuff
from django.db import models
from django.utils.timezone import now
from uuidfield import UUIDField

# Junction Stuff
from junction.base.models import TimeAuditModel


def expiry_time(expiry_mins=60):
    return now() + datetime.timedelta(minutes=expiry_mins)


class Device(TimeAuditModel):
    uuid = UUIDField(version=1, hyphenate=True, unique=True, db_index=True)

    # Verification
    is_verified = models.BooleanField(default=False)
    verification_code = models.IntegerField()
    verification_code_sent_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Verification Code Sent At")
    verification_code_expires_at = models.DateTimeField(
        verbose_name="Verification Code Expires At",
        default=expiry_time)

    def __unicode__(self):
        return u"uuid: {}, is_verified: {}".format(self.uuid,
                                                   self.is_verified)
