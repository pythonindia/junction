# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import csv

from django.contrib import admin
from django.http import HttpResponse


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
    list_display = (
        "created_at",
        "modified_at",
    )
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected as CSV"


class AuditAdmin(TimeAuditAdmin):
    list_display = ("created_by", "modified_by",) + TimeAuditAdmin.list_display
    exclude = (
        "created_by",
        "modified_by",
    )

    def save_model(self, request, obj, form, change):
        save_model(self, request, obj, form, change)
