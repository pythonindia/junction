from django import forms

from custom_utils.constants import PROPOSAL_TARGET_AUDIENCES, PROPOSAL_STATUS_LIST
from proposals.models import ConferenceProposalSection, ConferenceProposalType


def _get_proposal_section_choices(conference):
    return [(str(cps.id), cps.proposal_section.name)
            for cps in ConferenceProposalSection.objects.filter(conference=conference)]

def _get_proposal_type_choices(conference):
    return [(str(cpt.id), cpt.proposal_type.name)
            for cpt in ConferenceProposalType.objects.filter(conference=conference)]

class ProposalForm(forms.Form):
    '''
    Used for create/edit
    '''
    title = forms.CharField(min_length=10)
    description = forms.CharField(widget=forms.Textarea)
    target_audience = forms.ChoiceField(choices=PROPOSAL_TARGET_AUDIENCES, widget=forms.RadioSelect)
    prerequisites = forms.CharField(widget=forms.Textarea, required=False)
    content_urls = forms.CharField(widget=forms.Textarea, required=False)
    speaker_info = forms.CharField(widget=forms.Textarea, required=False)
    speaker_links = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(choices=PROPOSAL_STATUS_LIST, widget=forms.RadioSelect)
    proposal_type = forms.ChoiceField(widget=forms.RadioSelect)
    proposal_section = forms.ChoiceField(widget=forms.RadioSelect)

    def __init__(self, conference, *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields['proposal_section'].choices = _get_proposal_section_choices(conference)
        self.fields['proposal_type'].choices = _get_proposal_type_choices(conference)
