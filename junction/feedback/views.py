# -*- coding: utf-8 -*-

# Third Party Stuff
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from rest_framework import status, views
from rest_framework.response import Response

# Junction Stuff
from junction.schedule.models import ScheduleItem

from . import service as feedback_service
from .permissions import CanSubmitFeedBack, can_view_feedback
from .serializers import FeedbackQueryParamsSerializer, FeedbackSerializer


class FeedbackQuestionListApiView(views.APIView):
    def get(self, request):
        data = request.query_params
        obj = FeedbackQueryParamsSerializer(data=data)
        if obj.is_valid():
            data = feedback_service.get_feedback_questions(
                conference_id=obj.data['conference_id'])
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data=obj.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackListApiView(views.APIView):
    permission_classes = (CanSubmitFeedBack,)

    def post(self, request):
        feedback = FeedbackSerializer(data=request.data)
        if feedback.is_valid():
            data = feedback_service.has_required_fields_data(feedback)
            if data[0] is False:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'error': data[1]})
            if feedback_service.has_submitted(feedback,
                                              device_uuid=self.device_uuid):
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'error': 'Feedback already submitted'})
            data = feedback_service.create(feedback=feedback,
                                           device_uuid=self.device_uuid)
            return Response(status=status.HTTP_201_CREATED, data=data)
        return Response(data=feedback.errors,
                        status=status.HTTP_400_BAD_REQUEST)


def view_feedback(request, schedule_item_id):
    """Show text/choice feedback for the schedule.
    """
    schedule_item = get_object_or_404(ScheduleItem, pk=schedule_item_id)
    if not can_view_feedback(user=request.user,
                             schedule_item=schedule_item):
        return HttpResponseForbidden("Access Denied")
    feedback = feedback_service.get_feedback(schedule_item=schedule_item)
    context = {'feedback': feedback, 'schedule_item': schedule_item}
    return render(request, "feedback/detail.html", context)
