# Third Party Stuff
from django.contrib import admin  # noqa

from junction.conferences import service

from .models import ScheduleItem, ScheduleItemType


@admin.register(ScheduleItem)
class SchduleItemAdmin(admin.ModelAdmin):
    list_filter = ('type', 'room')

    def get_queryset(self, request):
        qs = super(SchduleItemAdmin, self).get_queryset(
            request)
        if request.user.is_superuser:
            return qs
        moderators = service.list_conference_moderator(user=request.user)
        return qs.filter(conference__in=[m.conference for m in moderators])


@admin.register(ScheduleItemType)
class SchduleItemTypeAdmin(admin.ModelAdmin):
    pass
