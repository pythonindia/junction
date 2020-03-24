# -*- coding: utf-8 -*-

import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from .. import factories

pytestmark = pytest.mark.django_db


# Create your tests here.


class TestFeedbackQuestionListApi(APITestCase):
    def setUp(self):
        self.schedule_item_types = ['Talk', 'Workshop']

    def test_get_questions_without_conference(self):
        res = self.client.get('/api/v1/feedback_questions/?conference_id=23')

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {}

    def test_get_questions(self):
        num_choice_questions = 2
        num_text_questions = 1
        objects = factories.create_feedback_questions(
            schedule_item_types=self.schedule_item_types,
            num_text_questions=num_text_questions,
            num_choice_questions=num_choice_questions)
        conference = objects['conference']

        res = self.client.get(
            '/api/v1/feedback_questions/?conference_id={}'.format(
                conference.id))

        assert res.status_code == status.HTTP_200_OK
        result = res.data

        for rest in list(result.keys()):
            assert rest in self.schedule_item_types
        for item_type in self.schedule_item_types:
            assert len(result[item_type]['text']) == num_text_questions
            assert len(result[item_type]['choice']) == num_choice_questions


class TestFeedbackListApi(APITestCase):
    def setUp(self):
        self.device = factories.create_device()
        self.schedule_item_types = ['Workshop', 'Talk']
        num_choice_questions = 1
        num_text_questions = 1
        self.objects = factories.create_feedback_questions(
            schedule_item_types=self.schedule_item_types,
            num_text_questions=num_text_questions,
            num_choice_questions=num_choice_questions)
        self.schedule_items = factories.create_schedule_items(
            conference=self.objects['conference'],
            item_types=self.schedule_item_types)

    def test_feedback_without_device_token(self):
        res = self.client.post('/api/v1/feedback/', {}, format='json')

        assert res.status_code == status.HTTP_403_FORBIDDEN

    def _submit_feedback(self):
        choice = [x for x in self.objects['choices']
                  if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        text = [x for x in self.objects['text']
                if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        schedule_item = [x for x in self.schedule_items
                         if x.type == self.schedule_item_types[0]][0]
        data = {'text': [{'id': text.id, 'text': 'Ok'}],
                'choices': [{'id': choice.id,
                             'value_id': choice.allowed_values.all()[0].id}],
                'schedule_item_id': schedule_item.id}

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.device.uuid))

        res = self.client.post('/api/v1/feedback/', data, format='json')
        """Data is sent in below format
        {'text': [{'text': 'Ok', 'id': 1}], 'schedule_item_id': 1,
        'choices': [{'id': 1, 'value_id': 1}]}
        """
        assert res.status_code == status.HTTP_201_CREATED
        assert len(res.data['text']) == 1
        assert len(res.data['choices']) == 1
        assert res.data['text'][0]['text'] == data['text'][0]['text']
        assert res.data['choices'][0]['value_id'] == data['choices'][0]['value_id']

    def test_submit_feedback(self):
        self._submit_feedback()

    def test_resubmit_feedback(self):
        self._submit_feedback()

        choice = [x for x in self.objects['choices']
                  if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        text = [x for x in self.objects['text']
                if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        schedule_item = [x for x in self.schedule_items
                         if x.type == self.schedule_item_types[0]][0]
        data = {'text': [{'id': text.id, 'text': 'Ok'}],
                'choices': [{'id': choice.id,
                             'value_id': choice.allowed_values.all()[0].id}],
                'schedule_item_id': schedule_item.id}

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.device.uuid))
        res = self.client.post('/api/v1/feedback/', data, format='json')

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data['error'] == 'Feedback already submitted'

    def test_feedback_with_proper_data(self):
        pass

    def test_feedback_with_wrong_choice_value(self):
        choice = [x for x in self.objects['choices']
                  if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        text = [x for x in self.objects['text']
                if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        schedule_item = [x for x in self.schedule_items
                         if x.type == self.schedule_item_types[0]][0]
        data = {'text': [{'id': text.id, 'text': 'Ok'}],
                'choices': [{'id': choice.id,
                             'value_id': 23}],
                'schedule_item_id': schedule_item.id}

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.device.uuid))
        res = self.client.post('/api/v1/feedback/', data, format='json')

        msg = u"The multiple choice value isn't associated with question"

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data == {'choices': [{u'non_field_errors':
                                         [msg]}]}

    def test_feedback_with_missing_required_text_data(self):
        choice = [x for x in self.objects['choices']
                  if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        schedule_item = [x for x in self.schedule_items
                         if x.type == self.schedule_item_types[0]][0]
        data = {'choices': [{'id': choice.id,
                             'value_id': choice.allowed_values.all()[0].id}],
                'schedule_item_id': schedule_item.id}

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.device.uuid))
        res = self.client.post('/api/v1/feedback/', data, format='json')

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data == {'error': 'Text Feedback is missing'}

    def test_feedback_with_missing_required_choice_data(self):
        text = [x for x in self.objects['text']
                if x.schedule_item_type.title == self.schedule_item_types[0]][0]
        schedule_item = [x for x in self.schedule_items
                         if x.type == self.schedule_item_types[0]][0]
        data = {'text': [{'id': text.id, 'text': 'Boom'}],
                'schedule_item_id': schedule_item.id}

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + str(self.device.uuid))
        res = self.client.post('/api/v1/feedback/', data, format='json')

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert res.data == {'error': 'Choice feedback is missing'}
