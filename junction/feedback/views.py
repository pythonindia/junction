# -*- coding: utf-8 -*-

from rest_framework import views, status
from rest_framework.response import Response

from .serializers import FeedbackQueryParamsSerializer
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
