from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.http.response import HttpResponseForbidden

from junction.base.constants import (
    PROPOSAL_STATUS_PUBLIC)
from junction.conferences.models import Conference

from .models import (
    Proposal,
    ProposalComment,
    ProposalSectionReviewer
)
from junction.conferences.models import (
    ConferenceProposalReviewer
)


@login_required
@require_http_methods(['GET'])
def proposals_dashboard(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    proposals_qs = Proposal.objects.filter(
        conference=conference,
        status=PROPOSAL_STATUS_PUBLIC)
    by_type = {}
    by_section = {}
    by_reviewer = {}
    by_audience = {}
    reviewed_count = 0
    unreviewed_count = 0
    for proposal in proposals_qs:
        pro_type = proposal.proposal_type
        section = proposal.proposal_section
        # dict structure {'id':[total, review, unreview, name]}
        by_type.setdefault(pro_type.id, [0, 0, 0, pro_type.name])
        by_type[pro_type.id][0] = by_type[pro_type.id][0] + 1
        by_section.setdefault(section.id, [0, 0, 0, section.name])
        by_section[section.id][0] = by_section[section.id][0] + 1
        private_comment_count = \
            ProposalComment.objects.filter(
                proposal=proposal,
                deleted=False,
                private=True).count()
        if private_comment_count:
            reviewed_count = reviewed_count + 1
            by_type[pro_type.id][1] = by_type[pro_type.id][1] + 1
            by_section[section.id][1] = by_section[section.id][1] + 1
        else:
            unreviewed_count = unreviewed_count + 1
            by_type[pro_type.id][2] = by_type[pro_type.id][2] + 1
            by_section[section.id][2] = by_section[section.id][2] + 1
    sections = \
        ProposalSectionReviewer.objects.filter(
            conference_reviewer__reviewer=request.user)\
        .distinct('proposal_section__id')
    # Hande case if reviewer is added to section twice'
    for section in sections:
        proposal_qs = proposals_qs.filter(proposal_section=section.proposal_section)
        # due to space and number issue for key used this
        key_id = '%s' % section.proposal_section.id
        by_reviewer.setdefault(
            key_id,
            [proposal_qs.count(), 0, 0, section.proposal_section.name])
        for proposal in proposal_qs:
            private_comment_count = ProposalComment.objects.filter(
                proposal=proposal, deleted=False, private=True).count()
            if private_comment_count:
                by_reviewer[key_id][1] = by_reviewer[key_id][1] + 1
            else:
                by_reviewer[key_id][2] = by_reviewer[key_id][2] + 1
    audience_dict = {
        1: 'Beginner',
        2: 'Intermediate',
        3: 'Advanced'
    }
    for proposal in proposals_qs:
        audience = audience_dict[proposal.target_audience]
        by_audience.setdefault(audience, [0, 0, 0, audience])
        private_comment_count = \
            ProposalComment.objects.filter(
                proposal=proposal,
                deleted=False,
                private=True).count()
        if private_comment_count:
            by_audience[audience][1] = by_audience[audience][1] + 1
            by_audience[audience][0] = by_audience[audience][0] + 1
        else:
            by_audience[audience][2] = by_audience[audience][2] + 1
            by_audience[audience][0] = by_audience[audience][0] + 1
    ctx = {
        'conference': conference,
        'total': proposals_qs.count(),
        'reviewed': reviewed_count,
        'unreviewed': unreviewed_count,
        'group_by_type': by_type,
        'group_by_section': by_section,
        'group_by_reviewer_section': by_reviewer,
        'by_target_audience': by_audience
    }
    return render(request, 'proposals/dashboard.html', ctx)


@login_required
@require_http_methods(['GET'])
def reviewer_comments_dashboard(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)

    if not request.user.is_superuser:
        return HttpResponseForbidden()
    conference_reviewers = ConferenceProposalReviewer.objects.filter(
        conference=conference, active=True)
    proposals_qs = Proposal.objects.filter(
        conference=conference,
        status=PROPOSAL_STATUS_PUBLIC)
    by_conference = {}
    by_section = {}
    for reviewers in conference_reviewers:
        id = reviewers.reviewer.id
        by_conference.setdefault(id, [reviewers.reviewer, 0])
        by_conference[id][1] = ProposalComment.objects.filter(
            commenter=reviewers.reviewer,
            deleted=False, private=True).count()
        # by_section is dict with
        # find each reviewers section and their comments
        # Need to rework on this code section to make it 1-2 loops
        by_section.setdefault(
            id,
            {'reviewer': reviewers.reviewer, 'interaction': []})
        reviewers_section = ProposalSectionReviewer.objects.filter(
            conference_reviewer=reviewers)
        for section in reviewers_section:
            proposal_qs = proposals_qs.filter(
                proposal_section=section.proposal_section)
            commented = 0
            uncommented = 0
            for proposal in proposal_qs:
                private_comment_count = ProposalComment.objects.filter(
                    proposal=proposal, deleted=False,
                    private=True, commenter=reviewers.reviewer).count()
                if private_comment_count:
                    commented = commented + 1
                else:
                    uncommented = uncommented + 1
            by_section[id]['interaction'].append(
                [
                    proposal_qs.count(), commented,
                    uncommented, section.proposal_section.name]
            )

    ctx = {
        'conference': conference,
        'conference_reviewers': conference_reviewers,
        'by_conference': by_conference,
        'by_section': by_section}

    return render(request, 'proposals/reviewers_dashboard.html', ctx)
