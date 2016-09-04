# Standard Library
from collections import OrderedDict

# Third Party Stuff
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect

# Junction Stuff
from junction.conferences.models import Conference

# Profile Stuff
from .models import Profile
from .forms import ProfileForm


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


@login_required
def profile(request):
    form = ProfileForm()
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.save()
            print "form saved"
            return HttpResponseRedirect("/profiles")
    elif request.method == "GET":
        return render(request, 'profiles/userprofile.html')
