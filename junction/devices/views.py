# -*- coding: utf-8 -*-

# Standard Library
import os
import random
import uuid

# Third Party Stuff
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import status, views
from rest_framework.response import Response
from six.moves import range

from .models import Device
from .serializers import DeviceConfirmationSerializer, DeviceRegistrationSerializer


# Create your views here.


class DeviceListApiView(views.APIView):
    def _create_device(self, data):
        if os.environ.get('TESTING'):
            code = settings.DEVICE_VERIFICATION_CODE
        else:
            code = random.choice(list(range(10000, 99999)))
        device = Device.objects.create(uuid=data['uuid'],
                                       verification_code=code)
        return device

    def post(self, request):
        obj = DeviceRegistrationSerializer(data=request.data)
        if obj.is_valid():
            if Device.objects.filter(uuid=obj.data['uuid']).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'uuid': 'Already registered'})
            else:
                device = self._create_device(data=obj.data)
                data = {'uuid': str(device.uuid)}
                return Response(status=status.HTTP_201_CREATED,
                                data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=obj.errors)


# TODO: This is required when verification code dispatch mechansim is decided


class DeviceDetailApiView(views.APIView):
    def _verify(self, device, code):
        if device.verification_code == code and \
           timezone.now() < device.verification_code_expires_at:
            device.is_verified = True
            device.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'code': 'Incorrect code'})

    def post(self, request, _uuid):
        obj = DeviceConfirmationSerializer(data=request.data)
        if obj.is_valid():
            try:
                device = Device.objects.get(uuid=uuid.UUID(_uuid))
                return self._verify(device=device, code=obj.data['code'])
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=obj.errors)
