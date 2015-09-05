# -*- coding: utf-8 -*-

import uuid

from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.


class TestDeviceListApiView(APITestCase):
    def test_register(self):
        data = {'uuid': str(uuid.uuid1())}
        res = self.client.post('/api/v1/devices/', data, format='json')

        assert res.status_code == status.HTTP_201_CREATED
        assert res.data == data

    # def test_verify_device(self):
    #     code = settings.DEVICE_VERIFICATION_CODE

    #     _uuid = uuid.uuid1()
    #     data = {'uuid': str(_uuid)}
    #     res = self.client.post('/api/v1/devices/', data, format='json')

    #     assert res.status_code == status.HTTP_201_CREATED

    #     url = '/api/v1/devices/{}/'.format(_uuid)

    #     resp = self.client.post(url, {'code': code},
    #                             format='json')

    #     assert resp.status_code == status.HTTP_200_OK
