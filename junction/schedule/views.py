# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template.loader import render_to_string

from rest_framework import viewsets, filters

from .models import ScheduleItem
from .serializers import ScheduleSerializer


class ScheduleView(viewsets.ReadOnlyModelViewSet):
    queryset = ScheduleItem.objects.all()
    serializer_class = ScheduleSerializer
    filter_backend = (filters.DjangoFilterBackend,)
    filter_fields = ('room', 'conference', 'event_date')


def dummy_schedule(request, conference_slug):
    data = render_to_string('dummy_schedule.json')
    return HttpResponse(data, content_type='application/json')
