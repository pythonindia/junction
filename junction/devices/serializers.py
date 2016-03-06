# -*- coding: utf-8 -*-

# Third Party Stuff
from rest_framework import serializers


class DeviceRegistrationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class DeviceConfirmationSerializer(serializers.Serializer):
    code = serializers.IntegerField()
