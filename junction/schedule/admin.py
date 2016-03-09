# Third Party Stuff
from django.contrib import admin  # noqa

from .models import ScheduleItem, ScheduleItemType


@admin.register(ScheduleItem)
class SchduleItemAdmin(admin.ModelAdmin):
    list_filter = ('type', 'room')


@admin.register(ScheduleItemType)
class SchduleItemTypeAdmin(admin.ModelAdmin):
    pass
