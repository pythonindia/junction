# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django import forms
from django.utils.safestring import mark_safe
from pagedown.widgets import PagedownWidget

# Junction Stuff
from junction.base.constants import (
    PROPOSAL_REVIEW_STATUS_LIST,
    PROPOSAL_STATUS_LIST,
    PROPOSAL_TARGET_AUDIENCES,
    PROPOSAL_REVIEW_VOTES_LIST
)
from junction.proposals.models import ProposalSection, ProposalType


def _get_proposal_section_choices(conference):
    return [(str(cps.id), cps.name)
            for cps in ProposalSection.objects.filter(conferences=conference)]


def _get_proposal_type_choices(conference):
    return [(str(cpt.id), cpt.name)
            for cpt in ProposalType.objects.filter(conferences=conference)]


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
    title = forms.CharField(min_length=10,
                            help_text="Title of the proposal, no buzz words!",
                            widget=forms.TextInput(attrs={'class': 'charfield'}))
    description = forms.CharField(widget=PagedownWidget(show_preview=True),
                                  help_text=("Describe your proposal with clear objective in simple sentence."
                                  " Keep it short and simple."))
    target_audience = forms.ChoiceField(
        choices=PROPOSAL_TARGET_AUDIENCES,
        widget=forms.Select(attrs={'class': 'dropdown'}))
    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'dropdown'}),
        choices=PROPOSAL_STATUS_LIST,
        help_text=("If you choose DRAFT people can't the see the session in the list."
                   " Make the proposal PUBLIC when you're done with editing the session."))
    proposal_type = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'dropdown'}))
    proposal_section = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'dropdown'}))

    # Additional Content
    prerequisites = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False,
        help_text="What should the participants know before attending your session?")
    content_urls = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False,
        help_text="Links to your session like GitHub repo, Blog, Slideshare etc ...")
    speaker_info = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False,
        help_text="Say something about yourself, work etc...")
    speaker_links = forms.CharField(
        widget=PagedownWidget(show_preview=True), required=False,
        help_text="Links to your previous work like Blog, Open Source Contributions etc ...")

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
    private = forms.BooleanField(required=False, widget=forms.HiddenInput())


class ProposalReviewForm(forms.Form):

    """
    Used to review the proposal.
    """
    review_status = forms.ChoiceField(
        choices=PROPOSAL_REVIEW_STATUS_LIST,
        widget=forms.RadioSelect()
    )


class ProposalReviewerVoteForm(forms.Form):

    """
    Used by ProposalSectionReviewers to vote on proposals.
    """
    vote_value = forms.ChoiceField(
        choices=PROPOSAL_REVIEW_VOTES_LIST,
        widget=forms.RadioSelect()
    )
