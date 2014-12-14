from django.contrib import admin

from conferences.models import Conference, ConferenceModerator, \
    ConferenceProposalReviewer
from custom_utils.admin import AuditAdmin


class ConferenceAdmin(AuditAdmin):
    list_display = ('name', 'start_date', 'end_date', 'status') + AuditAdmin.list_display


class ConferenceModeratorAdmin(AuditAdmin):
    list_display = ('conference', 'moderator', 'active') + AuditAdmin.list_display


class ConferenceProposallReviewerAdmin(AuditAdmin):
    list_display = ('conference', 'reviewer', 'active') + AuditAdmin.list_display


admin.site.register(Conference, ConferenceAdmin)
admin.site.register(ConferenceModerator, ConferenceModeratorAdmin)
admin.site.register(ConferenceProposalReviewer, ConferenceProposallReviewerAdmin)
