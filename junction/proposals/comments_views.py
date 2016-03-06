# -*- coding: utf-8 -*-

# Third Party Stuff
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import Http404, get_object_or_404
from django.views.decorators.http import require_http_methods

# Junction Stuff
from junction.conferences.models import Conference

from . import permissions
from .forms import ProposalCommentForm
from .models import Proposal, ProposalComment
from .services import send_mail_for_new_comment


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

        has_perm = permissions.is_proposal_author_or_proposal_section_reviewer(
            user=request.user, conference=conference, proposal=proposal)

        if private and not has_perm:
            raise Http404()

        proposal_comment = ProposalComment.objects.create(
            proposal=proposal, comment=comment,
            private=private, reviewer=reviewer, commenter=request.user
        )
        host = '{}://{}'.format(settings.SITE_PROTOCOL,
                                request.META.get('HTTP_HOST'))
        send_mail_for_new_comment(proposal_comment, host)

    redirect_url = reverse('proposal-detail',
                           args=[conference.slug, proposal.slug])

    if private:
        redirect_url += "#js-reviewers"
    elif reviewer:
        redirect_url += "#js-only-reviewers"
    else:
        redirect_url += "#js-comments"

    return HttpResponseRedirect(redirect_url)
