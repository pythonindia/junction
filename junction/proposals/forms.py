from django import forms
from django.utils.safestring import mark_safe
from pagedown.widgets import PagedownWidget

from custom_utils.constants import PROPOSAL_TARGET_AUDIENCES, PROPOSAL_STATUS_LIST
from proposals.models import ConferenceProposalSection, ConferenceProposalType


def _get_proposal_section_choices(conference):
    return [(str(cps.id), cps.proposal_section.name)
            for cps in ConferenceProposalSection.objects.filter(conference=conference)]


def _get_proposal_type_choices(conference):
    return [(str(cpt.id), cpt.proposal_type.name)
            for cpt in ConferenceProposalType.objects.filter(conference=conference)]


class HorizRadioRenderer(forms.RadioSelect.renderer):

    """
    This overrides widget method to put radio buttons horizontally instead of vertically.
    """

    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class ProposalForm(forms.Form):

    '''
    Used for create/edit
    '''
    title = forms.CharField(min_length=10)
    description = forms.CharField(widget=PagedownWidget(show_preview=True))
    target_audience = forms.ChoiceField(
        choices=PROPOSAL_TARGET_AUDIENCES, widget=forms.RadioSelect(renderer=HorizRadioRenderer))
    status = forms.ChoiceField(
        choices=PROPOSAL_STATUS_LIST, widget=forms.RadioSelect(renderer=HorizRadioRenderer))
    proposal_type = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=HorizRadioRenderer))
    proposal_section = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=HorizRadioRenderer))

    # Additional Content
    prerequisites = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False)
    content_urls = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False)
    speaker_info = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False)
    speaker_links = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False)

    def __init__(self, conference, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields['proposal_section'].choices = _get_proposal_section_choices(
            conference)
        self.fields['proposal_type'].choices = _get_proposal_type_choices(
            conference)

    @classmethod
    def populate_form_for_update(self, proposal):
        form = ProposalForm(proposal.conference,
                            initial={'title': proposal.title,
                                     'description': proposal.description,
                                     'target_audience': proposal.target_audience,
                                     'prerequisites': proposal.prerequisites,
                                     'content_urls': proposal.content_urls,
                                     'speaker_info': proposal.speaker_info,
                                     'speaker_links': proposal.speaker_links,
                                     'status': proposal.status,
                                     'proposal_section': proposal.proposal_section.pk,
                                     'proposal_type': proposal.proposal_type.pk, })
        return form


class ProposalCommentForm(forms.Form):

    '''
    Used to add comments
    '''
    comment = forms.CharField(widget=PagedownWidget(show_preview=True))
    private = forms.BooleanField(required=False)


class ProposalVoteForm(forms.Form):

    '''
    Used for csrf token in voting
    '''
    pass


class ProposalCommentVoteForm(forms.Form):

    '''
    Used for csrf token in voting
    '''
    pass
