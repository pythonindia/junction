from django.shortcuts import render

from junction.proposals.models import Proposal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(['GET'])
def dashboard(request):
    proposal_qs = Proposal.objects.order_by('conference__end_date')
    user_proposal_list = []
    if request.user.is_authenticated():
        user_proposal_list = proposal_qs.filter(author=request.user,
                                                deleted=False)
    return render(request, 'profiles/dashboard.html',
                  {'user_proposal_list': user_proposal_list})
