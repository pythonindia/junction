from django.contrib import admin

from junction.custom_utils.admin import AuditAdmin, TimeAuditAdmin
from junction.proposals.models import (
    Proposal,
    ProposalComment,
    ProposalCommentVote,
    ProposalSection,
    ProposalType,
    ProposalVote
)


class ProposalSectionAdmin(AuditAdmin):
    list_display = ('name', 'active') + AuditAdmin.list_display


class ProposalTypeAdmin(AuditAdmin):
    list_display = ('name', 'active') + AuditAdmin.list_display


class ProposalAdmin(TimeAuditAdmin):
    list_display = ('conference', 'proposal_section', 'proposal_type', 'author',
                    'title', 'slug', 'status', 'review_status') + TimeAuditAdmin.list_display


class ProposalVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal', 'voter', 'role', 'up_vote') + \
        TimeAuditAdmin.list_display


class ProposalCommentAdmin(TimeAuditAdmin):
    list_display = (
        'proposal', 'commenter', 'private', 'comment') + TimeAuditAdmin.list_display


class ProposalCommentVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal_comment', 'voter', 'up_vote') + \
        TimeAuditAdmin.list_display


admin.site.register(ProposalSection, ProposalSectionAdmin)
admin.site.register(ProposalType, ProposalTypeAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(ProposalVote, ProposalVoteAdmin)
admin.site.register(ProposalComment, ProposalCommentAdmin)
admin.site.register(ProposalCommentVote, ProposalCommentVoteAdmin)
