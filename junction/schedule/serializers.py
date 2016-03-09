# Third Party Stuff
from rest_framework import serializers

# Junction Stuff
from junction.proposals.serializers import ProposalSerializer

from .models import ScheduleItem


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    session = ProposalSerializer()
    room_id = serializers.PrimaryKeyRelatedField(source='room',
                                                 read_only=True)

    class Meta:
        model = ScheduleItem
        fields = ('room_id', 'event_date', 'start_time', 'end_time',
                  'name', 'session', 'type', 'conference', 'id')
