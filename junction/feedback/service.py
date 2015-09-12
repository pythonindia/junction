# -*- coding: utf-8 -*-

from collections import defaultdict

from .models import TextFeedbackQuestion, ChoiceFeedbackQuestion


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
