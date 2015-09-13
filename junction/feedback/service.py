# -*- coding: utf-8 -*-

from collections import defaultdict
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from junction.devices.models import Device


from .models import (TextFeedbackQuestion, ChoiceFeedbackQuestion,
                     ScheduleItemTextFeedback, ScheduleItemChoiceFeedback,
                     ChoiceFeedbackQuestionValue)


def get_feedback_questions(conference_id):
    """Get all feedback questions for the conference.

    {'talk': {'Text': [{'id': 1, 'title': 'How was the speaker ?',
    'is_required': True}], 'Workshop': [{'id': 1,
    'title': 'How was the content ?', 'is_required': True,
    allowed_values: [{'title': 'Awesome', 'id': 2},
    {'title': 'Bad', 'id': 3}, {'title': 'Ok', 'id': 4}}]}]
    }}
    """
    text_questions = get_text_feedback_questions(
        conference_id=conference_id)
    choice_questions = get_choice_feedback_questions(
        conference_id=conference_id)
    return _merge_questions(text_questions=text_questions,
                            choice_questions=choice_questions)


def get_text_feedback_questions(conference_id):
    """Get all text questions for the conference organized by
    schedule item type.

    Return dict contain all questions with schedule item type in dict.
    """
    qs = TextFeedbackQuestion.objects.filter(conference_id=conference_id)
    return _get_question_oragnized_by_type(qs)


def get_choice_feedback_questions(conference_id):
    """Get all choice based questions for the conference organized by
    schedule item type.
    """
    qs = ChoiceFeedbackQuestion.objects.filter(
        conference_id=conference_id).select_related('allowed_values')
    return _get_question_oragnized_by_type(qs)


def has_submitted(feedback, device_uuid):
    """
    """
    device = Device.objects.get(uuid=device_uuid)
    text_feedback = ScheduleItemTextFeedback.objects.filter(
        schedule_item_id=feedback.validated_data['schedule_item_id'],
        device=device)
    if text_feedback:
        return True
    choice_feedback = ScheduleItemChoiceFeedback.objects.filter(
        schedule_item_id=feedback.validated_data['schedule_item_id'],
        device=device)
    return choice_feedback


def create(feedback, device_uuid):
    device = Device.objects.get(uuid=device_uuid)
    try:
        with transaction.atomic():
            text = create_text_feedback(
                schedule_item_id=feedback.validated_data['schedule_item_id'],
                feedbacks=feedback.validated_data['text'],
                device=device)
            choices = create_choice_feedback(
                schedule_item_id=feedback.validated_data['schedule_item_id'],
                feedbacks=feedback.validated_data['choices'],
                device=device)
            return {'text': text, 'choices': choices}
    except (IntegrityError, ObjectDoesNotExist) as e:
        print(e)  # Replace with log
        return False


def create_text_feedback(schedule_item_id, feedbacks, device):
    text = []
    for feedback in feedbacks:
        obj = ScheduleItemTextFeedback.objects.create(
            schedule_item_id=schedule_item_id,
            question_id=feedback['id'],
            text=feedback['text'], device=device)
        d = {'id': obj.id, 'text': obj.text,
             'question_id': feedback['id'],
             'schedule_item_id': schedule_item_id}
        text.append(d)
    return text


def create_choice_feedback(schedule_item_id, feedbacks, device):
    choices = []
    for feedback in feedbacks:
        value = ChoiceFeedbackQuestionValue.objects.get(
            question_id=feedback['id'], id=feedback['value_id'])
        obj = ScheduleItemChoiceFeedback.objects.create(
            schedule_item_id=schedule_item_id, device=device,
            question_id=feedback['id'], value=value.value)
        d = {'id': obj.id, 'value_id': value.id,
             'question_id': feedback['id'],
             'schedule_item_id': schedule_item_id}
        choices.append(d)
    return choices


def _get_question_oragnized_by_type(qs):
    questions = defaultdict(list)
    for question in qs:
        questions[question.schedule_item_type.title].append(
            question.to_response())
    return questions


def _merge_questions(text_questions, choice_questions):
    """Merge the choice and text based questions into schedule type
    {'Talk': {'text': [..], 'choice': [...]},}
    """
    types = set(text_questions.keys())
    types.union(choice_questions.keys())
    questions = {}
    for item in types:
        questions[item] = {'text': text_questions.get(item),
                           'choice': choice_questions.get(item)}
    return questions
