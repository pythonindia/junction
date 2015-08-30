# -*- coding: utf-8 -*-

from collections import defaultdict

from django.http import HttpResponse
from django.template.loader import render_to_string

from rest_framework import viewsets, filters
from rest_framework.response import Response

from .models import ScheduleItem
from .serializers import ScheduleSerializer


class ScheduleView(viewsets.ReadOnlyModelViewSet):
    queryset = ScheduleItem.objects.all()
    serializer_class = ScheduleSerializer
    filter_backend = (filters.DjangoFilterBackend,)
    filter_fields = ('room', 'conference', 'event_date')

    def get_queryset(self):
        data = super(ScheduleView, self).get_queryset().prefetch_related(
            'session', 'session__proposal_type', 'session__proposal_section',
            'session__author').order_by('event_date', 'start_time')
        return data

    def list(self, request):
        data = self.get_queryset()
        schedule = defaultdict(dict)
        for datum in data:
            d = datum.to_response(request=request)
            start_time = d['start_time']
            event_date = d['event_date']
            try:
                schedule[event_date][start_time].append(d)
            except KeyError:
                schedule[event_date][start_time] = [d]
        return Response(schedule)


def dummy_schedule(request, conference_slug):
    data = render_to_string('dummy_schedule.json')
    return HttpResponse(data, content_type='application/json')
