# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
<<<<<<< HEAD

from junction.conferences.models import Conference, ConferenceProposalReviewer

<<<<<<< HEAD
=======
from conferences.models import Conference, ConferenceProposalReviewer
import json
>>>>>>> ProposalCommentVote
from proposals.forms import ProposalCommentForm, ProposalForm, ProposalVoteForm, ProposalCommentVoteForm
from proposals.models import Proposal, ProposalComment, ProposalVote, ProposalCommentVote
=======
from .forms import ProposalCommentForm, ProposalForm, ProposalVoteForm
from .models import Proposal, ProposalComment, ProposalVote, ProposalSection, ProposalType
>>>>>>> 9f9e0da3d0f742f5f41c4b83c42b1dae5ab328f1


def _is_proposal_author(user, proposal):
    if user.is_authenticated() and proposal.author == user:
        return True
    return False


def _is_proposal_reviewer(user, conference):
    if user.is_authenticated() and ConferenceProposalReviewer.objects.filter(reviewer=user,
                                                                             conference=conference,
                                                                             active=True):
        return True
    return False


def _is_proposal_author_or_reviewer(user, conference, proposal):
    return _is_proposal_author(user, proposal) or _is_proposal_reviewer(user, conference)


@require_http_methods(['GET'])
def list_proposals(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposals_list = Proposal.objects.filter(conference=conference)
    proposal_sections = ProposalSection.objects.filter(conferences=conference)
    proposal_types = ProposalType.objects.filter(conferences=conference)

    return render(request, 'proposals/list.html', {'proposals_list': proposals_list,
                                                   'proposal_sections': proposal_sections,
                                                   'proposal_types': proposal_types,
                                                   'conference': conference})


@login_required
@require_http_methods(['GET', 'POST'])
def create_proposal(request, conference_slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    if request.method == 'GET':
        form = ProposalForm(conference)
        return render(request, 'proposals/create.html', {'form': form,
                                                         'conference': conference, })

    # POST Workflow
    form = ProposalForm(conference, request.POST)

    if not form.is_valid():
        return render(request, 'proposals/create.html', {'form': form,
                                                         'conference': conference,
                                                         'errors': form.errors})

    # Valid Form
    Proposal.objects.create(author=request.user,
                            conference=conference,
                            title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            target_audience=form.cleaned_data[
                                'target_audience'],
                            prerequisites=form.cleaned_data['prerequisites'],
                            content_urls=form.cleaned_data['content_urls'],
                            speaker_info=form.cleaned_data['speaker_info'],
                            speaker_links=form.cleaned_data['speaker_links'],
                            status=form.cleaned_data['status'],
                            proposal_type_id=form.cleaned_data[
                                'proposal_type'],
                            proposal_section_id=form.cleaned_data[
                                'proposal_section']
                            )

    return HttpResponseRedirect(reverse('proposals-list',
                                        args=[conference.slug]))


@require_http_methods(['GET'])
def detail_proposal(request, conference_slug, slug):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=slug, conference=conference)
    allow_private_comment = _is_proposal_author_or_reviewer(
        request.user, conference, proposal)

    comments = ProposalComment.objects.filter(
        proposal=proposal, deleted=False).order_by("-created_at")
    if not allow_private_comment:
        comments = comments.filter(private=False)

    proposal_comment_form = ProposalCommentForm()
    proposal_vote_form = ProposalVoteForm()
    proposal_comment_vote_form = ProposalCommentVoteForm()
    
    can_delete = False
    if request.user == proposal.author:
        can_delete = True

    vote_value = 0

    try:
        if request.user.is_authenticated():
            proposal_vote = ProposalVote.objects.get(
                proposal=proposal, voter=request.user)
            vote_value = 1 if proposal_vote.up_vote else -1
    except ProposalVote.DoesNotExist:
        pass

<<<<<<< HEAD
    return render(request, 'proposals/detail.html', {'proposal': proposal,
                                                     'comments': comments,
                                                     'proposal_comment_form': proposal_comment_form,
                                                     'proposal_vote_form': proposal_vote_form,
                                                     'proposal_comment_vote_form': proposal_comment_vote_form,
                                                     'allow_private_comment': allow_private_comment,
                                                     'vote_value': vote_value,
                                                     'can_delete': can_delete})
=======
    ctx = {
        'proposal': proposal,
        'comments': comments,
        'proposal_comment_form': proposal_comment_form,
        'proposal_vote_form': proposal_vote_form,
        'allow_private_comment': allow_private_comment,
        'vote_value': vote_value,
        'can_delete': can_delete
    }

    return render(request, 'proposals/detail.html', ctx)
>>>>>>> 9f9e0da3d0f742f5f41c4b83c42b1dae5ab328f1


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

        ProposalComment.objects.create(proposal=proposal,
                                       comment=comment,
                                       private=private,
                                       commenter=request.user,
                                       )

    return HttpResponseRedirect(reverse('proposal-detail',
                                        args=[conference.slug, proposal.slug]))


def proposal_vote(request, conference_slug, proposal_slug, up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(
        Proposal, slug=proposal_slug, conference=conference)

    proposal_vote, created = ProposalVote.objects.get_or_create(proposal=proposal,  # @UnusedVariable
                                                                voter=request.user)

    role = 2 if _is_proposal_reviewer(request.user, conference) else 1

    proposal_vote.role = role
    proposal_vote.up_vote = up_vote
    proposal_vote.save()

    return HttpResponseRedirect(reverse('proposal-detail',
                                        args=[conference.slug, proposal.slug]))


@login_required
@require_http_methods(['POST'])
def proposal_vote_up(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, True)


@login_required
@require_http_methods(['POST'])
def proposal_vote_down(request, conference_slug, proposal_slug):
    return proposal_vote(request, conference_slug, proposal_slug, False)


def proposal_comment_vote(request, conference_slug, proposal_slug, comment_id, up_vote):
    conference = get_object_or_404(Conference, slug=conference_slug)
    proposal = get_object_or_404(Proposal, slug=proposal_slug, conference=conference)
    proposal_comment = get_object_or_404(ProposalComment, proposal=proposal, id=comment_id)
    
    proposal_comment_vote, created = ProposalCommentVote.objects.get_or_create(proposal_comment=proposal_comment,
                                                                               voter=request.user)
    
    proposal_comment_vote.up_vote = up_vote
    proposal_comment_vote.save()

    response_data = {'get_votes_count':proposal_comment.get_votes_count()}

    return HttpResponse(json.dumps(response_data), content_type='application/json') 
  
    
@login_required
@require_http_methods(['POST'])
def proposal_comment_vote_up(request, conference_slug, proposal_slug, proposal_comment_id):
    if request.is_ajax():
        return proposal_comment_vote(request, conference_slug, proposal_slug, proposal_comment_id, True)
    else:
        # A better Error message or Error Page should be displayed or it can be done in the front-end.
        return HttpResponse('The request is not ajax')    

@login_required
@require_http_methods(['POST'])
def proposal_comment_vote_down(request, conference_slug, proposal_slug, proposal_comment_id):
    if request.is_ajax():
        return proposal_comment_vote(request, conference_slug, proposal_slug, proposal_comment_id, False)
    else:
        # A better Error message or Error Page should be displayed.
        return HttpResponse('The request is not ajax')  
