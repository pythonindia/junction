from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from junction.base.constants import ProposalStatus
from junction.proposals import serializers
from junction.proposals.models import Proposal


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page'


class ProposalListApiView(generics.ListAPIView):

    serializer_class = serializers.ProposalListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Proposal.objects.filter(deleted=False, status=ProposalStatus.PUBLIC)
        conference = self.request.query_params.get('conference', None)
        if conference:
            queryset = queryset.filter(conference__slug=conference)
        return queryset
