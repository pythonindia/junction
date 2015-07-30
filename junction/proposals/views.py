# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import collections

# Third Party Stuff
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import Http404, get_object_or_404, render
from django.views.decorators.http import require_http_methods


# Junction Stuff
from junction.base.constants import ProposalReviewStatus, ProposalStatus, ConferenceStatus, ProposalUserVoteRole
from junction.conferences.models import Conference, ConferenceProposalReviewer

from .forms import (
    ProposalCommentForm,
    ProposalForm,
    ProposalReviewForm,
    ProposalReviewerVoteForm,
    ProposalsToReviewForm
)
from .models import (
    Proposal,
    ProposalComment,
    ProposalCommentVote,
    ProposalSectionReviewer,
    ProposalVote,
    ProposalSectionReviewerVote,
    ProposalSectionReviewerVoteValue
)
from .services import (
    send_mail_for_new_comment,
    send_mail_for_new_proposal,
    send_mail_for_proposal_content,
)


def _is_proposal_author(user, proposal):
    return user.is_authenticated() and proposal.author == user


def _is_proposal_reviewer(user, conference):
    return user.is_authenticated() and ConferenceProposalReviewer.objects.filter(
        reviewer=user, conference=conference, active=True).exists()


def _is_proposal_section_reviewer(user, conference, proposal):
    return user.is_authenticated() and ProposalSectionReviewer.objects.filter(
        conference_reviewer__reviewer=user,
        conference_reviewer__conference=conference,
        proposal_section=proposal.proposal_section,
        active=True).exists()


def _is_proposal_author_or_proposal_reviewer(user, conference, proposal):
    return _is_proposal_author(user, proposal) or \
        _is_proposal_reviewer(user, conference)


def _is_proposal_author_or_proposal_section_reviewer(user, conference, proposal):
    return _is_proposal_author(user, proposal) or \
        _is_proposal_section_reviewer(user, conference, proposal)


@require_http_methods(['GET'])
def list_proposals(request, conference_slug):
    conference = get_object_or_404(
        Conference, slug=conference_slug)
    # .prefetch_related('proposal_types', 'proposal_sections')

    proposals_qs = Proposal.objects.select_related(
        'proposal_type', 'proposal_section', 'conference', 'author',
    ).filter(conference=conference)

    is_reviewer = _is_proposal_reviewer(request.user, conference)

    # Filtering
    proposal_section_filter = request.GET.getlist('proposal_section')
    proposal_type_filter = request.GET.getlist('proposal_type')
    is_filtered = False

    if proposal_section_filter:
        proposals_qs = proposals_qs.filter(
            proposal_section__id__in=proposal_section_filter)
        is_filtered = True

    if proposal_type_filter:
        proposals_qs = proposals_qs.filter(
            proposal_type__id__in=proposal_type_filter)
        is_filtered = True

    # make sure it's after the tag filtering is applied
    selected_proposals_list = proposals_qs.filter(
        review_status=ProposalReviewStatus.SELECTED)

    # Display proposals which are public & exclude logged in user proposals
    if request.user.is_authenticated():
        proposals_qs = proposals_qs.exclude(author=request.user.id)

    public_proposals_list = proposals_qs.exclude(
        review_status=ProposalReviewStatus.SELECTED).filter(
            status=ProposalStatus.PUBLIC).order_by('-created_at')

    proposal_sections = conference.proposal_sections.all()
    proposal_types = conference.proposal_types.all()

    return render(request, 'proposals/list.html',
                  {'public_proposals_list': public_proposals_list,
                   'selected_proposals_list': selected_proposals_list,
                   'proposal_sections': proposal_sections,
                   'proposal_types': proposal_types,
                   'is_filtered': is_filtered,
                   'is_reviewer': is_reviewer,
                   'conference': conference,
                   'ConferenceStatus': ConferenceStatus})


@login_required
@require_http_methods(['GET', 'POST'])
def create_proposal(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    if request.method == 'GET':
        if not conference.is_accepting_proposals():
            return render(request, 'proposals/closed.html',
                          {'conference': conference})
        form = ProposalForm(conference, action="create",
                            initial={'status': ProposalStatus.PUBLIC})
        return render(request, 'proposals/create.html',
                      {'form': form,
                       'conference': conference, })

    # POST Workflow
    form = ProposalForm(conference, data=request.POST, action="create")

    if not form.is_valid():
        return render(request, 'proposals/create.html',
                      {'form': form,
                       'conference': conference,
                       'errors': form.errors})

    # Valid Form
    proposal = Proposal.objects.create(
        author=request.user,
        conference=conference,
        title=form.cleaned_data['title'],
        description=form.cleaned_data['description'],
        target_audience=form.cleaned_data['target_audience'],
        prerequisites=form.cleaned_data['prerequisites'],
        content_urls=form.cleaned_data['content_urls'],
        speaker_info=form.cleaned_data['speaker_info'],
        speaker_links=form.cleaned_data['speaker_links'],
        status=form.cleaned_data['status'],
        proposal_type_id=form.cleaned_data['proposal_type'],
        proposal_section_id=form.cleaned_data['proposal_section'])
    host = '{}://{}'.format(settings.SITE_PROTOCOL, request.META['HTTP_HOST'])
    send_mail_for_new_proposal(proposal, host)

    return HttpResponseRedirect(reverse('proposal-detail',
                                        args=[conference.slug, proposal.slug]))


@require_http_methods(['GET'])
def detail_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)
    read_private_comment = _is_proposal_author_or_proposal_reviewer(
        request.user, conference, proposal)
    write_private_comment = _is_proposal_author_or_proposal_section_reviewer(
        request.user, conference, proposal)
    is_reviewer = _is_proposal_reviewer(request.user, conference)
    is_section_reviewer = _is_proposal_section_reviewer(request.user, conference, proposal)
    vote_value = 0

    try:
        if request.user.is_authenticated():
            proposal_vote = ProposalVote.objects.get(
                proposal=proposal, voter=request.user)
            vote_value = 1 if proposal_vote.up_vote else -1
    except ProposalVote.DoesNotExist:
        pass

    ctx = {
        'login_url': settings.LOGIN_URL,
        'proposal': proposal,
        'read_private_comment': read_private_comment,
        'write_private_comment': write_private_comment,
        'vote_value': vote_value,
        'is_author': request.user == proposal.author,
        'is_reviewer': is_reviewer,
        'is_section_reviewer': is_section_reviewer,
    }

    comments = ProposalComment.objects.filter(
        proposal=proposal, deleted=False, vote=False
    )

    if read_private_comment:
        ctx['reviewers_comments'] = comments.get_reviewers_comments()
    if write_private_comment:
        ctx['reviewers_proposal_comment_form'] = ProposalCommentForm(
            initial={'private': True})
    if is_reviewer:
        ctx['reviewers_only_proposal_comment_form'] = ProposalCommentForm(
            initial={'reviewer': True})
        ctx['reviewers_only_comments'] = comments.get_reviewers_only_comments()
    ctx.update({'comments': comments.get_public_comments(),
                'proposal_comment_form': ProposalCommentForm()})

    return render(request, 'proposals/detail/base.html', ctx)


@login_required
@require_http_methods(['GET', 'POST'])
def update_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not proposal.author == request.user:
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = ProposalForm.populate_form_for_update(proposal)
        return render(request, 'proposals/update.html', {'form': form,
                                                         'proposal': proposal})

    # POST Workflow
    form = ProposalForm(conference, data=request.POST)
    if not form.is_valid():
        return render(request, 'proposals/update.html',
                      {'form': form,
                       'proposal': proposal,
                       'errors': form.errors})

    # Valid Form
    proposal.title = form.cleaned_data['title']
    proposal.description = form.cleaned_data['description']
    proposal.target_audience = form.cleaned_data['target_audience']
    proposal.prerequisites = form.cleaned_data['prerequisites']
    proposal.content_urls = form.cleaned_data['content_urls']
    proposal.speaker_info = form.cleaned_data['speaker_info']
    proposal.speaker_links = form.cleaned_data['speaker_links']
    proposal.status = form.cleaned_data['status']
    proposal.proposal_type_id = form.cleaned_data['proposal_type']
    proposal.proposal_section_id = form.cleaned_data['proposal_section']
    proposal.save()
    return HttpResponseRedirect(reverse('proposal-detail',
                                        args=[conference.slug, proposal.slug]))


@login_required
@require_http_methods(['GET', 'POST'])
def proposals_to_review(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)

    if not _is_proposal_reviewer(request.user, conference):
        return HttpResponseForbidden()

    proposals_qs = Proposal.objects.select_related(
        'proposal_type', 'proposal_section', 'conference', 'author',
    ).filter(conference=conference).filter(status=ProposalStatus.PUBLIC)

    proposal_reviewer_sections = [p.proposal_section for p in
                                  ProposalSectionReviewer.objects.filter(
                                      conference_reviewer__reviewer=request.user)]
    proposals_to_review = []
    s_items = collections.namedtuple('section_items', 'section proposals')
    for section in proposal_reviewer_sections:
        section_proposals = [p for p in proposals_qs if p.proposal_section == section]
        proposals_to_review.append(s_items(section, section_proposals))

    proposal_sections = conference.proposal_sections.all()
    proposal_types = conference.proposal_types.all()
    form = ProposalsToReviewForm(conference=conference)

    ctx = {
        'proposals_to_review': proposals_to_review,
        'proposal_sections': proposal_sections,
        'proposal_types': proposal_types,
        'conference': conference,
        'form': form,
    }

    return render(request, 'proposals/to_review.html', ctx)


@login_required
@require_http_methods(['GET', 'POST'])
def review_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not _is_proposal_section_reviewer(request.user, conference, proposal):
        return HttpResponseForbidden()

    if request.method == 'GET':

        comments = ProposalComment.objects.filter(proposal=proposal, deleted=False,)

        proposal_review_form = ProposalReviewForm(initial={'review_status': proposal.review_status})

        ctx = {
            'proposal': proposal,
            'proposal_review_form': proposal_review_form,
            'reviewers_comments': comments.get_reviewers_comments(),
            'reviewers_only_comments': comments.get_reviewers_only_comments(),
            'reviewers_proposal_comment_form': ProposalCommentForm(
                initial={'private': True}),
            'reviewers_only_proposal_comment_form': ProposalCommentForm(
                initial={'review': True}),
        }

        return render(request, 'proposals/review.html', ctx)

    # POST Workflow
    form = ProposalReviewForm(request.POST)
    if not form.is_valid():
        return render(request, 'proposals/review.html', {'form': form,
                                                         'proposal': proposal,
                                                         'form_errors': form.errors})

    # Valid Form
    proposal.review_status = form.cleaned_data['review_status']
    proposal.save()

    return HttpResponseRedirect(reverse('proposals-list', args=[conference.slug]))


@login_required
@require_http_methods(['POST'])
def proposal_upload_content(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not (_is_proposal_section_reviewer(request.user, conference, proposal) or
            request.user.is_superuser):
        return HttpResponseForbidden()

    host = '{}://{}'.format(settings.SITE_PROTOCOL, request.META['HTTP_HOST'])
    response = send_mail_for_proposal_content(conference, proposal, host)

    if response == 1:
        message = 'Email sent successfully.'
    else:
        message = 'There is problem in sending mail. Please contact conference chair.'

    return HttpResponse(message)


@login_required
@require_http_methods(['GET', 'POST'])
def proposal_reviewer_vote(request, conference_slug, proposal_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug,
                                 conference=conference)

    if not _is_proposal_section_reviewer(request.user, conference, proposal):
        return HttpResponseForbidden()

    vote_value = None

    try:
        vote = ProposalSectionReviewerVote.objects.get(
            proposal=proposal,
            voter=ProposalSectionReviewer.objects.get(
                conference_reviewer__reviewer=request.user,
                conference_reviewer__conference=conference,
                proposal_section=proposal.proposal_section),
        )
        vote_value = vote.vote_value.vote_value
    except ProposalSectionReviewerVote.DoesNotExist:
        vote = None

    try:
        vote_comment = ProposalComment.objects.get(
            proposal=proposal,
            commenter=request.user,
            vote=True,
            deleted=False,
        )
    except:
        vote_comment = None
    if request.method == 'GET':
        if vote_comment:
            proposal_vote_form = ProposalReviewerVoteForm(
                initial={'vote_value': vote_value,
                         'comment': vote_comment.comment})
        else:
            proposal_vote_form = ProposalReviewerVoteForm(
                initial={'vote_value': vote_value})
        ctx = {
            'proposal': proposal,
            'proposal_vote_form': proposal_vote_form,
            'vote': vote,
        }

        return render(request, 'proposals/vote.html', ctx)

    # POST Workflow
    form = ProposalReviewerVoteForm(request.POST)
    if not form.is_valid():
        return render(request, 'proposals/vote.html',
                      {'form': form,
                       'proposal': proposal,
                       'form_errors': form.errors})

    # Valid Form
    vote_value = form.cleaned_data['vote_value']
    comment = form.cleaned_data['comment']
    if not vote:
        vote = ProposalSectionReviewerVote.objects.create(
            proposal=proposal,
            voter=ProposalSectionReviewer.objects.get(
                conference_reviewer__reviewer=request.user,
                conference_reviewer__conference=conference,
                proposal_section=proposal.proposal_section),
            vote_value=ProposalSectionReviewerVoteValue.objects.get(
                vote_value=vote_value),
        )
    else:
        vote.vote_value = ProposalSectionReviewerVoteValue.objects.get(
            vote_value=vote_value)
        vote.save()
    if not vote_comment:
        vote_comment = ProposalComment.objects.create(
            proposal=proposal,
            commenter=request.user,
            comment=comment,
            vote=True,
        )
    else:
        vote_comment.comment = comment
        vote_comment.save()
    return HttpResponseRedirect(reverse('proposals-to-review',
                                        args=[conference.slug]))


@login_required
@require_http_methods(['GET', 'POST'])
def delete_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not proposal.author == request.user:
        return HttpResponseForbidden()

    if request.method == 'GET':
        return render(request, 'proposals/delete.html', {'proposal': proposal})
    elif request.method == 'POST':
        proposal.delete()
        return HttpResponseRedirect(reverse('proposals-list',
                                            args=[conference.slug]))


@login_required
@require_http_methods(['POST'])
def create_proposal_comment(request, conference_slug, proposal_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(
        Proposal, slug=proposal_slug, conference=conference)
    form = ProposalCommentForm(request.POST)
    if form.is_valid():
        comment = form.cleaned_data['comment']
        private = form.cleaned_data['private']
        reviewer = form.cleaned_data['reviewer']

        if private and not _is_proposal_author_or_proposal_section_reviewer(
                request.user, conference, proposal):
            raise Http404()

        proposal_comment = ProposalComment.objects.create(
            proposal=proposal, comment=comment,
            private=private, reviewer=reviewer, commenter=request.user
        )
        host = '{}://{}'.format(settings.SITE_PROTOCOL, request.META['HTTP_HOST'])
        send_mail_for_new_comment(proposal_comment, host)

    redirect_url = reverse('proposal-detail', args=[conference.slug, proposal.slug])

    if private:
        redirect_url += "#js-reviewers"
    elif reviewer:
        redirect_url += "#js-only-reviewers"
    else:
        redirect_url += "#js-comments"

    return HttpResponseRedirect(redirect_url)


@login_required
def proposal_vote(request, conference_slug, proposal_slug, up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(
        Proposal, slug=proposal_slug, conference=conference)

    proposal_vote, created = ProposalVote.objects.get_or_create(
        proposal=proposal, voter=request.user)  # @UnusedVariable

    if _is_proposal_reviewer(request.user, conference):
        role = ProposalUserVoteRole.REVIEWER
    else:
        role = ProposalUserVoteRole.PUBLIC

    proposal_vote.role = role
    proposal_vote.up_vote = up_vote
    proposal_vote.save()

    return HttpResponse(proposal.get_votes_count())


@login_required
@require_http_methods(['POST'])
def proposal_vote_up(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, True)


@login_required
@require_http_methods(['POST'])
def proposal_vote_down(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, False)


def proposal_comment_vote(request, conference_slug, proposal_slug, comment_id,
                          up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug,
                                 conference=conference)
    proposal_comment = get_object_or_404(ProposalComment, proposal=proposal,
                                         id=comment_id)
    proposal_comment_vote, created = ProposalCommentVote.objects.get_or_create(
        proposal_comment=proposal_comment, voter=request.user)
    proposal_comment_vote.up_vote = up_vote
    proposal_comment_vote.save()

    return HttpResponseRedirect(reverse('proposal-detail',
                                        args=[conference.slug, proposal.slug]))


@login_required
@require_http_methods(['POST'])
def proposal_comment_up_vote(request, conference_slug, proposal_slug,
                             proposal_comment_id):
    return proposal_comment_vote(request, conference_slug, proposal_slug,
                                 proposal_comment_id, True)


@login_required
@require_http_methods(['POST'])
def proposal_comment_down_vote(request, conference_slug, proposal_slug,
                               proposal_comment_id):
    return proposal_comment_vote(request, conference_slug, proposal_slug,
                                 proposal_comment_id, False)
