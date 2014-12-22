from django import forms

from custom_utils.constants import PROPOSAL_TARGET_AUDIENCES, PROPOSAL_STATUS_LIST


class ProposalForm(forms.Form):
    '''
    Used for create/edit
    '''
    title = forms.CharField(min_length=10)
    description = forms.CharField(widget=forms.Textarea)
    target_audience = forms.ChoiceField(choices=PROPOSAL_TARGET_AUDIENCES)
    prerequisites = forms.CharField(widget=forms.Textarea, required=False)
    content_urls = forms.CharField(widget=forms.Textarea, required=False)
    speaker_info = forms.CharField(widget=forms.Textarea, required=False)
    speaker_links = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(choices=PROPOSAL_STATUS_LIST)
    proposal_type = forms.ChoiceField(choices=[])
    proposal_section = forms.ChoiceField(choices=[])

    def clean_proposal_type(self):
        return self.cleaned_data['proposal_type']

    def clean_proposal_section(self):
        return self.cleaned_data['proposal_section']
