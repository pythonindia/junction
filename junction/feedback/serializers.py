# -*- coding: utf-8 -*-

from rest_framework import serializers


class FeedbackQueryParamsSerializer(serializers.Serializer):
    conference_id = serializers.IntegerField()
