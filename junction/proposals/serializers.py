# Third Party Stuff
from rest_framework import serializers

from .models import Proposal, ProposalSection, ProposalType


class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    section = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_section(self, proposal):
        return proposal.proposal_section.name

    def get_type(self, proposal):
        return proposal.proposal_type.name

    def get_author(self, proposal):
        author = proposal.author
        return "{} {}".format(
            author.first_name, author.last_name).strip() or author.username

    class Meta:
        model = Proposal
        fields = ('title', 'section', 'type', 'author',
                  'slug', 'description', 'target_audience',
                  'prerequisites', 'content_urls', 'speaker_info',
                  'speaker_links')


class ProposalFilterSerializer(serializers.Serializer):
    proposal_section = serializers.PrimaryKeyRelatedField(queryset=ProposalSection.objects.all(), required=False)
    proposal_type = serializers.PrimaryKeyRelatedField(queryset=ProposalType.objects.all(), required=False)
