from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from conferences.models import Conference
from proposals.forms import ProposalForm
from proposals.models import Proposal, ProposalSection, ProposalType


try:
    conference = Conference.objects.get(pk=1)  # TODO: Remove it
except:
    pass  # Create it

@require_http_methods(['GET'])
def list_proposals(request):
    proposals_list = Proposal.objects.all()
    return render(request, 'proposals/list.html', {'proposals_list' : proposals_list, })

@login_required
@require_http_methods(['GET', 'POST'])
def create_proposal(request):

    if request.method == 'GET':
        form = ProposalForm(conference)
        return render(request, 'proposals/create.html', {'form':form, })

    form = ProposalForm(conference, request.POST)

    if not form.is_valid():
        return render(request, 'proposals/create.html', {'form':form, 'errors':form.errors, })

    Proposal.objects.create(author=request.user,
                            conference=conference,
                            title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            target_audience=form.cleaned_data['target_audience'],
                            prerequisites=form.cleaned_data['prerequisites'],
                            content_urls=form.cleaned_data['content_urls'],
                            speaker_info=form.cleaned_data['speaker_info'],
                            speaker_links=form.cleaned_data['speaker_links'],
                            status=form.cleaned_data['status'],
                            proposal_type=ProposalType.objects.get(id=int(form.cleaned_data['proposal_type'])),
                            proposal_section=ProposalSection.objects.get(id=int(form.cleaned_data['proposal_section']))
                            )

    return HttpResponseRedirect(reverse('proposals-list'))

@require_http_methods(['GET'])
def detail_proposal(request, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)  # TODO: Send 404 for incorrect ID
    if request.user == proposal.author:
        return render(request, 'proposals/detail.html', {'proposal':proposal, 'flag':1})
    else:
        return render(request, 'proposals/detail.html', {'proposal':proposal, 'flag':0})

@require_http_methods(['GET', 'POST'])
def update_proposal(request, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    if request.method == 'GET':
        form = ProposalForm.populate_form_for_update(proposal)

        return render(request, 'proposals/update.html', {'form':form})

    form = ProposalForm(conference, request.POST)

    if not form.is_valid():
        return render(request, 'proposals/update.html', {'form':form, 'errors':form.errors, })

    proposal.title=form.cleaned_data['title']
    proposal.description=form.cleaned_data['description']
    proposal.target_audience=form.cleaned_data['target_audience']
    proposal.prerequisites=form.cleaned_data['prerequisites']
    proposal.content_urls=form.cleaned_data['content_urls']
    proposal.speaker_info=form.cleaned_data['speaker_info']
    proposal.speaker_links=form.cleaned_data['speaker_links']
    proposal.status=form.cleaned_data['status']
    proposal.proposal_type.pk=form.cleaned_data['proposal_type']
    proposal.proposal_section.pk=form.cleaned_data['proposal_section']
    proposal.save()
    return HttpResponseRedirect(reverse('proposals-list'))

@require_http_methods(['GET', 'POST'])
def delete_proposal(request, proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    if request.method == 'GET':
        return render(request, 'proposals/delete.html', {'proposal':proposal})
    elif request.method == 'POST':
        proposal.delete()
        return HttpResponseRedirect(reverse('proposals-list'))
