# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

# Standard Library
import collections
import uuid
import io

# Third Party Stuff
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from xlsxwriter.workbook import Workbook

# Junction Stuff
from junction.base.constants import (
    ProposalReviewVote,
    ProposalStatus,
    ProposalReviewStatus,
)
from junction.conferences.models import Conference, ConferenceProposalReviewer

from .forms import ProposalVotesFilterForm
from .permissions import is_conference_moderator
from .utils import _sort_proposals_for_dashboard
from .models import (
    Proposal,
    ProposalComment,
    ProposalSectionReviewer,
    ProposalSectionReviewerVoteValue
)

from . import services
from . import permissions


@login_required
@require_http_methods(['GET'])
def proposals_dashboard(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)

    if not is_conference_moderator(user=request.user, conference=conference):
        raise PermissionDenied

    proposals_qs = Proposal.objects.filter(
        conference=conference,
        status=ProposalStatus.PUBLIC)

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
        proposal_qs = proposals_qs.filter(
            proposal_section=section.proposal_section)
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

    if not is_conference_moderator(user=request.user, conference=conference):
        raise PermissionDenied
    conference_reviewers = ConferenceProposalReviewer.objects.filter(
        conference=conference, active=True)
    proposals_qs = Proposal.objects.filter(
        conference=conference,
        status=ProposalStatus.PUBLIC)
    by_conference = {}
    by_section = {}
    for reviewers in conference_reviewers:
        id = reviewers.reviewer.id
        by_conference.setdefault(id, [reviewers.reviewer, 0])
        by_conference[id][1] = ProposalComment.objects.filter(
            commenter=reviewers.reviewer,
            deleted=False, private=True,
            proposal__status=ProposalStatus.PUBLIC,
            proposal__conference=conference).distinct('proposal').count()
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


@require_http_methods(['GET', 'POST'])
def reviewer_votes_dashboard(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    user = request.user
    if not is_conference_moderator(user=request.user, conference=conference):
        raise PermissionDenied

    proposal_sections = conference.proposal_sections.all()
    proposals_qs = Proposal.objects.select_related(
        'proposal_type', 'proposal_section', 'conference', 'author',
    ).filter(conference=conference, status=ProposalStatus.PUBLIC)

    proposals = []
    s_items = collections.namedtuple('section_items', 'section proposals')
    form = ProposalVotesFilterForm(conference=conference)

    if request.method == 'GET':
        for section in proposal_sections:
            section_proposals = [
                p for p in proposals_qs if p.proposal_section == section]
            proposals.append(s_items(section, section_proposals))

        return render(request, 'proposals/votes-dashboard.html',
                      {'conference': conference,
                       'proposals': proposals,
                       'form': form})

    form = ProposalVotesFilterForm(conference=conference, data=request.POST)

    if not form.is_valid():
        return render(request, 'proposals/votes-dashboard.html',
                      {'form': form,
                       'conference': conference,
                       'errors': form.errors})

    # Valid form

    proposals = _sort_proposals_for_dashboard(conference, proposals_qs, user, form)

    return render(request, 'proposals/votes-dashboard.html',
                  {'conference': conference,
                   'proposals': proposals,
                   'form': form})


@require_http_methods(['GET', 'POST'])
def second_phase_voting(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    user = request.user

    if not permissions.is_proposal_reviewer(request.user, conference):
        raise PermissionDenied

    proposal_sections = conference.proposal_sections.all()
    proposals_qs = Proposal.objects.select_related(
        'proposal_type', 'proposal_section', 'conference', 'author',
    ).filter(
        conference=conference,
        review_status=ProposalReviewStatus.SELECTED
    )

    proposals = []
    s_items = collections.namedtuple('section_items', 'section proposals')
    form = ProposalVotesFilterForm(conference=conference)

    if request.method == 'GET':
        for section in proposal_sections:
            section_proposals = [
                p for p in proposals_qs if p.proposal_section == section]
            proposals.append(s_items(section, section_proposals))

        return render(request, 'proposals/second_phase_voting.html',
                      {'conference': conference,
                       'proposals': proposals,
                       'form': form})

    form = ProposalVotesFilterForm(conference=conference, data=request.POST)

    if not form.is_valid():
        return render(request, 'proposals/votes-dashboard.html',
                      {'form': form,
                       'conference': conference,
                       'errors': form.errors})

    # Valid form
    proposals = _sort_proposals_for_dashboard(conference, proposals_qs, user, form)

    return render(request, 'proposals/second_phase_voting.html',
                  {'conference': conference,
                   'proposals': proposals,
                   'form': form})


@require_http_methods(['GET', 'POST'])
def export_reviewer_votes(request, conference_slug):
    """
    Write reviewer votes to a spreadsheet.
    """
    conference = get_object_or_404(Conference, slug=conference_slug)

    if not is_conference_moderator(user=request.user, conference=conference):
        raise PermissionDenied

    proposal_sections = conference.proposal_sections.all()
    proposals_qs = Proposal.objects.select_related(
        'proposal_type', 'proposal_section', 'conference', 'author',
    ).filter(conference=conference, status=ProposalStatus.PUBLIC)
    proposals_qs = sorted(
        proposals_qs, key=lambda x: x.get_reviewer_votes_sum(), reverse=True)
    vote_values_list = ProposalSectionReviewerVoteValue.objects.order_by(
        '-vote_value')
    vote_values_list = [v.vote_value for v in vote_values_list]
    vote_values_desc = tuple(i.description
                             for i in ProposalSectionReviewerVoteValue.objects.order_by('-vote_value'))
    header = ('Proposal Type', 'Title', 'Sum of reviewer votes', 'No. of reviewer votes') + \
        tuple(vote_values_desc) + ('Public votes count', 'Vote Comments')
    output = io.BytesIO()

    with Workbook(output) as book:
        for section in proposal_sections:
            sheet = book.add_worksheet(section.name[:30])
            cell_format = book.add_format({'bold': True})
            sheet.write_row(0, 0, header, cell_format)

            section_proposals = [
                p for p in proposals_qs if p.proposal_section == section]

            for index, p in enumerate(section_proposals, 1):
                vote_details = tuple(p.get_reviewer_votes_count_by_value(v)
                                     for v in vote_values_list)
                vote_comment = '\n'.join([comment.comment for comment in
                                          p.proposalcomment_set.filter(
                                              vote=True, deleted=False,)])
                row = (p.proposal_type.name, p.title, p.get_reviewer_votes_sum(),
                       p.get_reviewer_votes_count(),) + \
                    vote_details + (p.get_votes_count(), vote_comment,)
                if p.get_reviewer_votes_count_by_value(
                        ProposalSectionReviewerVoteValue.objects.get(
                            vote_value=ProposalReviewVote.NOT_ALLOWED).vote_value) > 0:
                    cell_format = book.add_format({'bg_color': 'red'})
                elif p.get_reviewer_votes_count_by_value(
                        ProposalSectionReviewerVoteValue.objects.get(
                            vote_value=ProposalReviewVote.MUST_HAVE).vote_value) > 2:
                    cell_format = book.add_format({'bg_color': 'green'})
                elif p.get_reviewer_votes_count() < 2:
                    cell_format = book.add_format({'bg_color': 'yellow'})
                else:
                    cell_format = None

                sheet.write_row(index, 0, row, cell_format)

    output.seek(0)
    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    file_name = str(uuid.uuid4())[:8]
    response['Content-Disposition'] = "attachment; filename=junction-{}.xlsx".format(file_name)

    return response


@login_required
@require_http_methods(['GET'])
def proposal_state(request, conference_slug):
    conf = get_object_or_404(Conference, slug=conference_slug)

    if not is_conference_moderator(user=request.user, conference=conf):
        raise PermissionDenied

    state = request.GET.get('q', 'unreviewed')
    proposals = services.group_proposals_by_reveiew_state(conf=conf, state=state)
    return render(request, 'proposals/review_state.html',
                  {'conference': conf,
                   'proposals': dict(proposals),
                   'state': state.title()})
