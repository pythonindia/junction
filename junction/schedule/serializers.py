from rest_framework import serializers

from junction.proposals.serializers import ProposalSerializer

from .models import ScheduleItem


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    session = ProposalSerializer()

    class Meta:
        model = ScheduleItem
        fields = ('room', 'event_date', 'start_time', 'end_time',
                  'name', 'session', 'type', 'conference')
