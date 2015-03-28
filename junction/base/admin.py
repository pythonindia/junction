# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin


def save_model(self, request, obj, form, change):
    """ Overriding this to update created_by & modified by users """
    instance = form.save(commit=False)
    if not instance.created_at and not instance.modified_at:
        instance.created_by = request.user
    instance.modified_by = request.user
    instance.save()
    form.save_m2m()
    return instance


class TimeAuditAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'modified_at',)


class AuditAdmin(TimeAuditAdmin):
    list_display = ('created_by', 'modified_by',) + TimeAuditAdmin.list_display
    exclude = ('created_by', 'modified_by',)

    def save_model(self, request, obj, form, change):
        save_model(self, request, obj, form, change)
