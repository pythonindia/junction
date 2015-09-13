# -*- coding: utf-8 -*-

import pytest

from rest_framework import status
from rest_framework.test import APITestCase

from .. import factories

pytestmark = pytest.mark.django_db


# Create your tests here.


class TestFeedbackQuestionListApi(APITestCase):
    def test_get_questions_without_conference(self):
        res = self.client.get('/api/v1/feedback_questions/?conference_id=23')

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {}

    def test_get_questions(self):
        schedule_item_types = ['Workshop', 'Talk']
        num_choice_questions = 2
        num_text_questions = 1
        objects = factories.create_feedback_questions(
            schedule_item_types=schedule_item_types,
            num_text_questions=num_text_questions,
            num_choice_questions=num_choice_questions)
        conference = objects['conference']

        res = self.client.get(
            '/api/v1/feedback_questions/?conference_id={}'.format(
                conference.id))

        assert res.status_code == status.HTTP_200_OK
        result = res.data

        assert result.keys() == schedule_item_types
        for item_type in schedule_item_types:
            assert len(result[item_type]['text']) == num_text_questions
            assert len(result[item_type]['choice']) == num_choice_questions


class TestFeedbackListApi(APITestCase):
    def test_feedback_without_device_token(self):
        res = self.client.post('/api/v1/feedback/', {}, format='json')

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def test_submit_feedback(self):
        device = factories.create_device()
        schedule_item_types = ['Workshop', 'Talk']
        num_choice_questions = 1
        num_text_questions = 1
        objects = factories.create_feedback_questions(
            schedule_item_types=schedule_item_types,
            num_text_questions=num_text_questions,
            num_choice_questions=num_choice_questions)
        schedule_item = factories.create_schedule_item(
            conference=objects['conference'])

        choice = objects['choices'][0]
        text = objects['text'][0]
        data = {'text': [{'id': text.id, 'text': 'Ok'}],
                'choices': [{'id': objects['choices'][0].id,
                             'value_id': choice.allowed_values.all()[0].id}],
                'schedule_item_id': schedule_item.id}

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(device.uuid))
        res = self.client.post('/api/v1/feedback/', data, format='json')

        assert res.status_code == status.HTTP_201_CREATED
        assert len(res.data['text']) == 1
        assert len(res.data['choices']) == 1
        assert res.data['text'][0]['text'] == data['text'][0]['text']
        assert res.data['choices'][0]['value_id'] == data['choices'][0]['value_id']

    def test_resubmit_feedback(self):
        device = factories.create_device()
        schedule_item_types = ['Workshop', 'Talk']
        num_choice_questions = 1
        num_text_questions = 1
        objects = factories.create_feedback_questions(
            schedule_item_types=schedule_item_types,
            num_text_questions=num_text_questions,
            num_choice_questions=num_choice_questions)
        schedule_item = factories.create_schedule_item(
            conference=objects['conference'])

        choice = objects['choices'][0]
        text = objects['text'][0]
        data = {'text': [{'id': text.id, 'text': 'Ok'}],
                'choices': [{'id': objects['choices'][0].id,
                             'value_id': choice.allowed_values.all()[0].id}],
                'schedule_item_id': schedule_item.id}

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(device.uuid))
        res = self.client.post('/api/v1/feedback/', data, format='json')

        assert res.status_code == status.HTTP_201_CREATED

    def test_feedback_with_proper_data(self):
        pass

    def test_feedback_with_wrong_data(self):
        pass
