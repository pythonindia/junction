# -*- coding: utf-8 -*-

from rest_framework import views, status
from rest_framework.response import Response

from .serializers import FeedbackQueryParamsSerializer, FeedbackSerializer
from .permissions import CanSubmitFeedBack
from . import service as feedback_service


# Create your views here.


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
            if feedback_service.has_submitted(feedback,
                                              device_uuid=self.device_uuid):
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'error': 'Feedback already submitted'})
            data = feedback_service.create(feedback=feedback,
                                           device_uuid=self.device_uuid)
            return Response(status=status.HTTP_201_CREATED, data=data)
        return Response(data=feedback.errors,
                        status=status.HTTP_400_BAD_REQUEST)
