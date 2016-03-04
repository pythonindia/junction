# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .models import Conference, ConferenceVenue, Room
from .serializers import ConferenceSerializer, RoomSerializer, VenueSerializer

from rest_framework import filters, viewsets


class ConferenceView(viewsets.ReadOnlyModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class VenueView(viewsets.ReadOnlyModelViewSet):
    queryset = ConferenceVenue.objects.all()
    serializer_class = VenueSerializer


class RoomView(viewsets.ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backend = (filters.DjangoFilterBackend,)
    filter_fields = ('venue',)
