# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from django_filters import rest_framework as filters

from .models import Conference, ConferenceVenue, Room
from .serializers import ConferenceSerializer, RoomSerializer, VenueSerializer


class ConferenceView(viewsets.ReadOnlyModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class VenueView(viewsets.ReadOnlyModelViewSet):
    queryset = ConferenceVenue.objects.all()
    serializer_class = VenueSerializer


class RoomView(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.DjangoFilterBackend,]
    filter_fields = ("venue",)


@require_http_methods(["GET"])
def get_conference(request, conference_slug):
    # if the conference does not exist, render 404
    get_object_or_404(Conference, slug=conference_slug)

    # redirect to <conference_slug>/proposals else
    return HttpResponseRedirect(
        reverse("proposals-list", kwargs={"conference_slug": conference_slug})
    )
