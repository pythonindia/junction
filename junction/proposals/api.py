from rest_framework import generics

from junction.base.constants import ProposalStatus
from junction.proposals import serializers
from junction.proposals.models import Proposal


class ProposalListApiView(generics.ListAPIView):

    serializer_class = serializers.ProposalListSerializer

    def get_queryset(self):
        queryset = Proposal.objects.filter(deleted=False, status=ProposalStatus.PUBLIC)
        conference = self.request.query_params.get('conference', None)
        if conference:
            queryset = queryset.filter(conference__slug=conference)
        return queryset
