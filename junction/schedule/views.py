# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.


def dummy_schedule(request, conference_slug):
    data = render_to_string('dummy_schedule.json')
    return HttpResponse(data, content_type='application/json')
