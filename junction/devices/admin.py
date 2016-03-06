# -*- coding: utf-8 -*-

# Third Party Stuff
from django.contrib import admin

# Junction Stuff
from junction.base.admin import TimeAuditAdmin

from .models import Device


# Register your models here.


class DeviceAdmin(TimeAuditAdmin):
    list_display = ('uuid', 'verification_code',
                    'verification_code_sent_at') + TimeAuditAdmin.list_display


admin.site.register(Device, DeviceAdmin)
