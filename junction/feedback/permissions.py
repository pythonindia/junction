# -*- coding: utf-8 -*-

# Standard Library
import uuid

# Third Party Stuff
from rest_framework import permissions

# Junction Stuff
from junction.conferences.permissions import is_reviewer
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
                return Device.objects.filter(uuid=view.device_uuid).exists()
            return False
        return False


def can_view_feedback(user, schedule_item):
    """Given a schedule item object, say a requesting user can view the
    feedback.
    """
    if user.is_superuser:
        return True

    session = schedule_item.session
    res = is_reviewer(user=user, conference=schedule_item.conference)
    return session and (session.author == user or res)
