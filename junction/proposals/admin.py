# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget
from simple_history.admin import SimpleHistoryAdmin

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
    list_display = ('name', 'active') + AuditAdmin.list_display


class ProposalSectionReviewerAdmin(AuditAdmin):
    list_display = ('conference_reviewer', 'proposal_section') + AuditAdmin.list_display
    list_filter = ['proposal_section']


class ProposalTypeAdmin(AuditAdmin):
    list_display = ('name', 'active', 'start_date', 'end_date') + AuditAdmin.list_display


class ProposalAdmin(TimeAuditAdmin, SimpleHistoryAdmin):
    list_display = ('proposal_info', 'author_info', 'author_email', 'conference',
                    'status', 'review_status', )
    list_filter = ['proposal_section__name', 'proposal_type',
                   'target_audience', 'conference', 'status', 'review_status']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }

    def proposal_info(self, obj):
        return '%s (%s)' % (obj.title, obj.proposal_type)

    def author_email(self, obj):
        if obj.author:
            return obj.author.email

    def author_info(self, obj):
        if obj.author:
            return "%s (%s)" % (obj.author.get_full_name(), obj.author.username)


class ProposalVoteAdmin(TimeAuditAdmin):
    list_display = ('proposal', 'voter', 'role', 'up_vote') + \
        TimeAuditAdmin.list_display


class ProposalSectionReviewerVoteValueAdmin(AuditAdmin):
    list_display = ('vote_value', 'description') + AuditAdmin.list_display


class ProposalSectionReviewerVoteAdmin(TimeAuditAdmin):
    list_filter = ['vote_value', 'proposal__proposal_type__name']
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
