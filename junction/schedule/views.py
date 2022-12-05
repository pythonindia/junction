# -*- coding: utf-8 -*-

from collections import OrderedDict, defaultdict

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import Http404, render
from django.template.loader import render_to_string
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .models import ScheduleItem
from .serializers import ScheduleSerializer


class ScheduleView(viewsets.ReadOnlyModelViewSet):
    queryset = ScheduleItem.objects.all()
    serializer_class = ScheduleSerializer
    filter_backend = (filters.DjangoFilterBackend,)
    filter_fields = ("room", "conference", "event_date")

    def get_queryset(self):
        data = (
            super(ScheduleView, self)
            .get_queryset()
            .prefetch_related(
                "session",
                "session__proposal_type",
                "session__proposal_section",
                "session__author",
            )
            .order_by("event_date", "start_time")
        )
        return self.filter_queryset(data)

    def list(self, request):
        data = self.get_queryset()
        schedule = defaultdict(OrderedDict)
        for datum in data:
            d = datum.to_response(request=request)
            key = "{} - {}".format(d["start_time"], d["end_time"])
            event_date = d["event_date"]
            try:
                schedule[event_date][key].append(d)
            except KeyError:
                schedule[event_date][key] = [d]
        return Response(schedule)


def dummy_schedule(request, conference_slug):
    data = render_to_string("dummy_schedule.json")
    return HttpResponse(data, content_type="application/json")


def non_proposal_schedule_item_view(request, sch_item_id):
    try:
        sch_item = ScheduleItem.objects.get(pk=sch_item_id)
        return render(
            request, "proposals/detail/schedule-item.html", {"sch_item": sch_item}
        )
    except ObjectDoesNotExist:
        raise Http404()
