from rest_framework import serializers

from .models import ScheduleItem


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScheduleItem
        fields = ('room', 'event_date', 'start_time', 'end_time',
                  'name', 'session', 'conference')
