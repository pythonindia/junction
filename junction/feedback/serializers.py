# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import (TextFeedbackQuestion, ChoiceFeedbackQuestion,
                     ChoiceFeedbackQuestionValue)


def object_exists(model, pk):
    if not model.objects.filter(pk=pk):
        raise serializers.ValidationError(
            "The question doesn't exist")
    return True


class FeedbackQueryParamsSerializer(serializers.Serializer):
    conference_id = serializers.IntegerField()


class TextFeedbackSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()

    def validate(self, data):
        if object_exists(TextFeedbackQuestion, pk=data['id']):
            return data


class ChoiceFeedbackSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value_id = serializers.IntegerField()

    def validate(self, data):
        if object_exists(ChoiceFeedbackQuestion, pk=data['value_id']):
            if ChoiceFeedbackQuestionValue.objects.filter(
                    question_id=data['id'], pk=data['value_id']).exists():
                return data
            raise serializers.ValidationError(
                "The question doesn't exist")


class FeedbackSerializer(serializers.Serializer):
    schedule_item_id = serializers.IntegerField()
    text = TextFeedbackSerializer(many=True, required=False)
    choices = ChoiceFeedbackSerializer(many=True, required=False)
