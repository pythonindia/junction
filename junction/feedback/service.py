# -*- coding: utf-8 -*-

# Standard Library
from collections import defaultdict

# Third Party Stuff
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.db.models import Count

# Junction Stuff
from junction.devices.models import Device
from junction.schedule.models import ScheduleItem, ScheduleItemType

from .models import (
    ChoiceFeedbackQuestion,
    ChoiceFeedbackQuestionValue,
    ScheduleItemChoiceFeedback,
    ScheduleItemTextFeedback,
    TextFeedbackQuestion
)

COLORS = ["#46BFBD", "#FDB45C", "#F7464A"]


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


def _has_required_ids(master, submitted):
    for item in master:
        if item not in submitted:
            return False
    return True


def has_required_fields_data(feedback):
    try:
        data = feedback.validated_data
        sch = ScheduleItem.objects.get(pk=data['schedule_item_id'])
        sch_type = ScheduleItemType.objects.get(
            title=sch.type)

        t_ids = TextFeedbackQuestion.objects.filter(
            schedule_item_type=sch_type,
            conference=sch.conference, is_required=True).values_list(
                'id', flat=True)

        if not data.get('text'):
            if t_ids:
                return False, "Text Feedback is missing"
        else:
            submitted_t_ids = {d['id'] for d in data.get('text')}

            if not _has_required_ids(master=t_ids, submitted=submitted_t_ids):
                return False, "Required text questions are missing"

        c_ids = ChoiceFeedbackQuestion.objects.filter(
            schedule_item_type=sch_type,
            conference=sch.conference, is_required=True).values_list(
                'id', flat=True)

        if not data.get('choices'):
            if c_ids:
                return False, "Choice feedback is missing"
        else:
            submitted_c_ids = {d['id'] for d in data.get('choices')}

            if not _has_required_ids(master=c_ids, submitted=submitted_c_ids):
                return False, "Choice feedback is missing"
        return True, ""
    except ObjectDoesNotExist as e:
        print(e)
        return False


def create(feedback, device_uuid):
    device = Device.objects.get(uuid=device_uuid)
    schedule_item_id = feedback.validated_data['schedule_item_id']
    try:
        with transaction.atomic():
            text, choices = [], []
            if feedback.validated_data.get('text'):
                text = create_text_feedback(
                    schedule_item_id=schedule_item_id,
                    feedbacks=feedback.validated_data.get('text'),
                    device=device)
            if feedback.validated_data.get('choices'):
                choices = create_choice_feedback(
                    schedule_item_id=schedule_item_id,
                    feedbacks=feedback.validated_data.get('choices'),
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


def get_feedback(schedule_item):
    feedback = {'text': _get_text_feedback(schedule_item=schedule_item),
                'choices': _get_choice_feedback(
                    schedule_item=schedule_item)}
    return feedback


def _get_text_feedback(schedule_item):
    questions = TextFeedbackQuestion.objects.filter(
        schedule_item_type__title=schedule_item.type)
    text = [{'question': question,
             'values': ScheduleItemTextFeedback.objects.filter(
                 question=question, schedule_item=schedule_item)}
            for question in questions]
    return text


def _get_choice_feedback(schedule_item):
    questions = ChoiceFeedbackQuestion.objects.filter(
        schedule_item_type__title=schedule_item.type).select_related(
            'allowed_values')
    choices = []
    for question in questions:
        values = ScheduleItemChoiceFeedback.objects.filter(
            schedule_item=schedule_item, question=question).values(
                'value').annotate(Count('value'))
        d = {'question': question,
             'values': _get_choice_value_for_chart(question=question,
                                                   values=values)}
        choices.append(d)
    return choices


def _get_choice_value_for_chart(question, values):
    data = []
    for index, value in enumerate(values):
        d = {'label': str(question.allowed_values.get(
            value=value['value']).title)}
        d['value'] = value['value__count']
        d['color'] = COLORS[index]
        data.append(d)
    return data


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
    types.union(list(choice_questions.keys()))
    questions = {}
    for item in types:
        questions[item] = {'text': text_questions.get(item),
                           'choice': choice_questions.get(item)}
    return questions
