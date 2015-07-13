from rest_framework import serializers

from .models import Proposal


class ProposalSerializer(serializers.HyperlinkedModelSerializer):
    section = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_section(self, proposal):
        return proposal.proposal_section.name

    def get_type(self, proposal):
        return proposal.proposal_type.name

    def get_author(self, proposal):
        return "{} {}".format(proposal.author.first_name,
                              proposal.author.first_name)

    class Meta:
        model = Proposal
        fields = ('conference', 'title', 'section', 'type', 'author',
                  'slug', 'description', 'target_audience',
                  'prerequisites', 'content_urls', 'speaker_info',
                  'speaker_links', 'status', 'review_status')
