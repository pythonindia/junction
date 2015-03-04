# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import Http404, get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from junction.base.constants import PROPOSAL_REVIEW_STATUS_SELECTED
from junction.conferences.models import Conference, ConferenceProposalReviewer

from .forms import ProposalCommentForm, ProposalForm, ProposalReviewForm
from .models import (Proposal, ProposalComment, ProposalVote, ProposalSection,
                     ProposalType, ProposalCommentVote, ProposalSectionReviewer)
from .services import (send_mail_for_new_comment, send_mail_for_new_proposal,
                       post_tweet_for_new_proposal)


# Third Party Stuff
# Junction Stuff
def _is_proposal_author(user, proposal):
    if user.is_authenticated() and proposal.author == user:
        return True
    return False


def _is_proposal_reviewer(user, conference):
    if user.is_authenticated() and ConferenceProposalReviewer.objects.filter(
            reviewer=user, conference=conference, active=True):
        return True
    return False


def _is_proposal_author_or_reviewer(user, conference, proposal):
    return _is_proposal_author(user, proposal) or _is_proposal_reviewer(
        user, conference)


@require_http_methods(['GET'])
def list_proposals(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)

    proposals_qs = Proposal.objects.filter(conference=conference)

    user_proposals_list = []
    if request.user.is_authenticated():  # Display the proposals by this user
        user_proposals_list = proposals_qs.filter(author=request.user)

    selected_proposals_list = proposals_qs.filter(review_status=PROPOSAL_REVIEW_STATUS_SELECTED)

    proposals_to_review = []
    if _is_proposal_reviewer(request.user, conference):
        proposal_reviewer_sections = [p.proposal_section for p in
                                      ProposalSectionReviewer.objects.filter(
                                          conference_reviewer__reviewer=request.user)]
        proposals_to_review = [p for p in proposals_qs
                               if p.proposal_section in proposal_reviewer_sections]

    # Filtering
    proposal_section_filter = request.GET.getlist('proposal_section')
    proposal_type_filter = request.GET.getlist('proposal_type')
    is_filtered = False

    if proposal_section_filter:
        proposals_qs = proposals_qs.filter(proposal_section__id__in=proposal_section_filter)
        is_filtered = True

    if proposal_type_filter:
        proposals_qs = proposals_qs.filter(proposal_type__id__in=proposal_type_filter)
        is_filtered = True

    public_proposals_list = proposals_qs.filter(~Q(review_status=PROPOSAL_REVIEW_STATUS_SELECTED))

    proposal_sections = ProposalSection.objects.filter(conferences=conference)
    proposal_types = ProposalType.objects.filter(conferences=conference)

    return render(request, 'proposals/list.html',
                  {'public_proposals_list': public_proposals_list,
                   'user_proposals_list': user_proposals_list,
                   'selected_proposals_list': selected_proposals_list,
                   'proposals_to_review': proposals_to_review,
                   'proposal_sections': proposal_sections,
                   'proposal_types': proposal_types,
                   'is_filtered': is_filtered,
                   'conference': conference})


@login_required
@require_http_methods(['GET', 'POST'])
def create_proposal(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    if request.method == 'GET':
        if conference.status != 1:
            return render(request, 'proposals/closed.html',
                          {'conference': conference})
        form = ProposalForm(conference)
        return render(request, 'proposals/create.html',
                      {'form': form,
                       'conference': conference, })

    # POST Workflow
    form = ProposalForm(conference, request.POST)

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
    post_tweet_for_new_proposal(proposal.title, proposal.get_absolute_url())
    return HttpResponseRedirect(reverse('proposals-list',
                                        args=[conference.slug]))


@require_http_methods(['GET'])
def detail_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)
    allow_private_comment = _is_proposal_author_or_reviewer(request.user, conference, proposal)

    vote_value = 0

    try:
        if request.user.is_authenticated():
            proposal_vote = ProposalVote.objects.get(proposal=proposal, voter=request.user)
            vote_value = 1 if proposal_vote.up_vote else -1
    except ProposalVote.DoesNotExist:
        pass

    ctx = {
        'proposal': proposal,
        'allow_private_comment': allow_private_comment,
        'vote_value': vote_value,
        'can_delete': request.user == proposal.author,
        'is_author': request.user == proposal.author,
    }

    comments = ProposalComment.objects.filter(
        proposal=proposal, deleted=False,
    )

    if allow_private_comment:
        ctx.update({
            'reviewers_comments': comments.filter(private=True),
            'reviewers_proposal_comment_form': ProposalCommentForm(
                initial={'private': True})
        })
    ctx.update({'comments': comments.filter(private=False),
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
    form = ProposalForm(conference, request.POST)
    if not form.is_valid():
        return render(request, 'proposals/update.html', {'form': form,
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
    return HttpResponseRedirect(reverse('proposals-list',
                                        args=[conference.slug]))


@login_required
@require_http_methods(['GET', 'POST'])
def review_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)

    if not _is_proposal_reviewer(request.user, conference):
        return HttpResponseForbidden()

    if request.method == 'GET':

        comments = ProposalComment.objects.filter(
            proposal=proposal, deleted=False,
        )

        proposal_review_form = ProposalReviewForm(
            initial={'review_status': proposal.review_status})

        ctx = {
            'proposal': proposal,
            'proposal_review_form': proposal_review_form,
            'reviewers_comments': comments.filter(private=True),
            'reviewers_proposal_comment_form': ProposalCommentForm(
                initial={'private': True}),
        }

        return render(request, 'proposals/review.html', ctx)

    # POST Workflow
    form = ProposalReviewForm(request.POST)
    if not form.is_valid():
        return render(request, 'proposals/review.html', {'form': form,
                                                         'proposal': proposal,
                                                         'errors': form.errors})

    # Valid Form
    proposal.review_status = form.cleaned_data['review_status']
    proposal.save()
    return HttpResponseRedirect(reverse('proposals-list',
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

        if private and not _is_proposal_author_or_reviewer(
                request.user, conference, proposal):
            raise Http404()

        proposal_comment = ProposalComment.objects.create(
            proposal=proposal, comment=comment,
            private=private, commenter=request.user)
        send_mail_for_new_comment(
            proposal_comment, login_url=settings.LOGIN_URL,
            host='{}://{}'.format(settings.SITE_PROTOCOL,
                                  request.META['HTTP_HOST']))

    redirect_url = reverse('proposal-detail',
                           args=[conference.slug, proposal.slug])

    redirect_url += "#js-reviewers" if private else "#js-comments"

    return HttpResponseRedirect(redirect_url)


@login_required
def proposal_vote(request, conference_slug, proposal_slug, up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)

    proposal_vote, created = ProposalVote.objects.get_or_create(
        proposal=proposal, voter=request.user)  # @UnusedVariable

    role = 2 if _is_proposal_reviewer(request.user, conference) else 1

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
