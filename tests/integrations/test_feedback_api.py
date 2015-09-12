# -*- coding: utf-8 -*-

import pytest

from rest_framework import status
from rest_framework.test import APITestCase

from .. import factories

pytestmark = pytest.mark.django_db


# Create your tests here.


class TestFeedQuestionListApiView(APITestCase):
    def test_get_questions_without_conference(self):
        res = self.client.get('/api/v1/feedback_questions/?conference_id=23')

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {}

    def test_get_questions(self):
        schedule_item_types = ['Workshop', 'Talk']
        num_choice_questions = 2
        num_text_questions = 1
        conference = factories.create_feedback_questions(
            schedule_item_types=schedule_item_types,
            num_text_questions=num_text_questions,
            num_choice_questions=num_choice_questions)

        res = self.client.get(
            '/api/v1/feedback_questions/?conference_id={}'.format(
                conference.id))

        assert res.status_code == status.HTTP_200_OK
        result = res.data

        assert result.keys() == schedule_item_types
        for item_type in schedule_item_types:
            assert len(result[item_type]['text']) == num_text_questions
            assert len(result[item_type]['choice']) == num_choice_questions
