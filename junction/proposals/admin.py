# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

# Junction Stuff
from junction.base.admin import AuditAdmin, TimeAuditAdmin
from junction.proposals.models import (
    Proposal,
    ProposalComment,
    ProposalCommentVote,
    ProposalSection,
    ProposalSectionReviewer,
    ProposalType,
    ProposalVote,
    ProposalSectionReviewerVote,
    ProposalSectionReviewerVoteValue
)


class ProposalSectionAdmin(AuditAdmin):
    list_display = ('name', 'active', 'start_date', 'end_date') + AuditAdmin.list_display


class ProposalSectionReviewerAdmin(AuditAdmin):
    list_display = ('conference_reviewer', 'proposal_section') + AuditAdmin.list_display


class ProposalTypeAdmin(AuditAdmin):
    list_display = ('name', 'active') + AuditAdmin.list_display


class ProposalAdmin(TimeAuditAdmin):
    list_display = ('conference', 'proposal_section', 'proposal_type', 'author',
                    'title', 'slug', 'status', 'review_status') + TimeAuditAdmin.list_display
    list_filter = ['proposal_section__name', 'target_audience']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }


class ProposalVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal', 'voter', 'role', 'up_vote') + \
        TimeAuditAdmin.list_display


class ProposalSectionReviewerVoteValueAdmin(AuditAdmin):
    list_display = ('vote_value', 'description') + AuditAdmin.list_display


class ProposalSectionReviewerVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal', 'voter', 'role', 'vote_value') + \
        TimeAuditAdmin.list_display


class ProposalCommentAdmin(TimeAuditAdmin):
    list_display = (
        'proposal', 'commenter', 'private', 'comment') + TimeAuditAdmin.list_display
    list_filter = ['private', 'reviewer']


class ProposalCommentVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal_comment', 'voter', 'up_vote') + \
        TimeAuditAdmin.list_display


admin.site.register(ProposalSection, ProposalSectionAdmin)
admin.site.register(ProposalType, ProposalTypeAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(ProposalVote, ProposalVoteAdmin)
admin.site.register(ProposalSectionReviewerVote, ProposalSectionReviewerVoteAdmin)
admin.site.register(ProposalSectionReviewerVoteValue, ProposalSectionReviewerVoteValueAdmin)
admin.site.register(ProposalComment, ProposalCommentAdmin)
admin.site.register(ProposalCommentVote, ProposalCommentVoteAdmin)
admin.site.register(ProposalSectionReviewer, ProposalSectionReviewerAdmin)
