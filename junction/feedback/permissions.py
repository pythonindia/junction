# -*- coding: utf-8 -*-

import uuid

from rest_framework import permissions

from junction.devices.models import Device


def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION')
    return auth


class CanSubmitFeedBack(permissions.BasePermission):
    def has_permission(self, request, view):
        token = get_authorization_header(request)
        if token:
            device_uuid = token.split()[-1]
            view.device_uuid = uuid.UUID(device_uuid)
            if device_uuid:
                return Device.objects.filter(
                    uuid=view.device_uuid).exists()
            return False
        return False
