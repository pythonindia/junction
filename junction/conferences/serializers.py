from rest_framework import serializers

from .models import Conference, ConferenceVenue, Room


class ConferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conference
        fields = ('name', 'slug', 'description', 'start_date',
                  'end_date', 'status', 'venue')


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConferenceVenue
        fields = ('name', 'address')


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'venue')
