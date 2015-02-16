# Third Party Stuff
from django.contrib import admin

# Junction Stuff
from junction.base.admin import AuditAdmin

from . import models


class ConferenceAdmin(AuditAdmin):
    list_display = ('name', 'slug', 'start_date', 'end_date', 'status') + AuditAdmin.list_display
    prepopulated_fields = {'slug': ('name',), }


class ConferenceModeratorAdmin(AuditAdmin):
    list_display = ('conference', 'moderator', 'active') + AuditAdmin.list_display


class ConferenceProposallReviewerAdmin(AuditAdmin):
    list_display = ('conference', 'reviewer', 'active') + AuditAdmin.list_display


admin.site.register(models.Conference, ConferenceAdmin)
admin.site.register(models.ConferenceModerator, ConferenceModeratorAdmin)
admin.site.register(models.ConferenceProposalReviewer, ConferenceProposallReviewerAdmin)
