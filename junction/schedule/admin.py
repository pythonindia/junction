from django.contrib import admin  # noqa

from .models import ScheduleItem


@admin.register(ScheduleItem)
class SchduleItemAdmin(admin.ModelAdmin):
    list_filter = ('type', 'room')
