from collections import OrderedDict

from django.shortcuts import render

from junction.conferences.models import Conference
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(['GET'])
def dashboard(request):
    conf_proposals = OrderedDict()
    for conf in Conference.objects.order_by('end_date'):
        for proposal in conf.proposal_set.filter(author=request.user).all():
            if conf.name in conf_proposals:
                conf_proposals[conf.name].append(proposal)
            else:
                conf_proposals[conf.name] = [proposal]
    return render(request, 'profiles/dashboard.html',
                  {'conf_proposals': conf_proposals})
