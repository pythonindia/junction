# -*- coding: utf-8 -*-

import pytest

from junction.feedback import service

from .. import factories

pytestmark = pytest.mark.django_db


def test_get_feedback_questions_without_conference():
    result = service.get_feedback_questions(conference_id=23)
    assert result == {}


def test_get_feedback_questions_with_conference():
    schedule_item_types = set(['Workshop', 'Talk'])
    num_choice_questions = 2
    num_text_questions = 1
    objects = factories.create_feedback_questions(
        schedule_item_types=schedule_item_types,
        num_text_questions=num_text_questions,
        num_choice_questions=num_choice_questions,
    )

    conference = objects['conference']
    result = service.get_feedback_questions(conference_id=conference.id)

    assert set(result.keys()) == schedule_item_types
    for item_type in schedule_item_types:
        assert len(result[item_type]['text']) == num_text_questions
        assert len(result[item_type]['choice']) == num_choice_questions
