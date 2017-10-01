# Standard Library
from collections import OrderedDict

# Third Party Stuff
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Junction Stuff
from junction.conferences.models import Conference

# Profile Stuff
from .models import Profile
from .forms import ProfileForm


@login_required
@require_http_methods(['GET'])
def dashboard(request):
    conf_proposals = OrderedDict()
    for conf in Conference.objects.order_by('-end_date'):
        for proposal in conf.proposal_set.filter(author=request.user).all():
            if conf.name in conf_proposals:
                conf_proposals[conf.name].append(proposal)
            else:
                conf_proposals[conf.name] = [proposal]
    return render(request, 'profiles/dashboard.html',
                  {'conf_proposals': conf_proposals})


@login_required
def profile(request):
    username = request.user
    detail = None

    if request.method == "POST" and username == request.user:
        user = User.objects.get(pk=username.id)
        detail = Profile.objects.filter(user=user).exists()
        if detail:
            detail = Profile.objects.get(user=user)
            detail_form = ProfileForm(request.POST, instance=detail)
            if detail_form.is_valid():
                detail = detail_form.save()
                return HttpResponseRedirect(reverse('profiles:dashboard'))
        else:
            user = User.objects.get(pk=username.id)
            detail_form = ProfileForm(request.POST)
            if detail_form.is_valid():
                detail_form = detail_form.save(commit=False)
                detail_form.user = user
                detail_form.save()
                return HttpResponseRedirect(reverse('profiles:dashboard'))

    elif request.method == "GET":
        user = User.objects.get(pk=username.id)
        detail = Profile.objects.filter(user=user).exists()
        if detail:
            detail = Profile.objects.get(user=user)
            return render(request, 'profiles/userprofile.html', {'detail': detail})
        else:
            return render(request, 'profiles/userprofile.html')
