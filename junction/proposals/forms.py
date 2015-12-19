# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django import forms
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from pagedown.widgets import PagedownWidget

# Junction Stuff
from junction.base.constants import (
    ProposalReviewStatus,
    ProposalStatus,
    ProposalTargetAudience,
    ProposalReviewerComment,
    ProposalVotesFilter,
)
from junction.proposals.models import (
    ProposalSection,
    ProposalType,
    ProposalSectionReviewerVoteValue
)


def _get_proposal_section_choices(conference, action="edit"):
    if action == "create":
        return [(str(cps.id), cps.name)
                for cps in ProposalSection.objects.filter(
                    conferences=conference)]
    else:
        return [(str(cps.id), cps.name)
                for cps in ProposalSection.objects.filter(
                    conferences=conference)]


def _get_proposal_type_choices(conference, action='edit'):
    if action == "create":
        return [(str(cpt.id), cpt.name)
                for cpt in ProposalType.objects.filter(
                    conferences=conference, end_date__gt=now())]
    else:
        return [(str(cpt.id), cpt.name)
                for cpt in ProposalType.objects.filter(
                    conferences=conference)]


def _get_proposal_section_reviewer_vote_choices():
    return [(i.vote_value, '{} ({})'.format(i.description, i.vote_value))
            for i in ProposalSectionReviewerVoteValue.objects.exclude(vote_value=0)]


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
        choices=ProposalTargetAudience.CHOICES,
        widget=forms.Select(attrs={'class': 'dropdown'}))
    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'dropdown'}),
        choices=ProposalStatus.CHOICES,
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

    def __init__(self, conference, action="edit", *args, **kwargs):
        super(ProposalForm, self).__init__(*args, **kwargs)
        self.fields['proposal_section'].choices = _get_proposal_section_choices(
            conference, action=action)
        self.fields['proposal_type'].choices = _get_proposal_type_choices(
            conference, action=action)

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
    reviewer = forms.BooleanField(required=False, widget=forms.HiddenInput())


class ProposalReviewForm(forms.Form):

    """
    Used to review the proposal.
    """
    review_status = forms.ChoiceField(
        choices=ProposalReviewStatus.CHOICES,
        widget=forms.RadioSelect()
    )


class ProposalReviewerVoteForm(forms.Form):

    """
    Used by ProposalSectionReviewers to vote on proposals.
    """
    vote_value = forms.ChoiceField(widget=forms.RadioSelect(),
                                   choices=_get_proposal_section_reviewer_vote_choices())
    comment = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Leave a comment justifying your vote.",
    )


class ProposalTypesChoices(forms.Form):
    """
    Base proposal form with proposal sections & types.
    """
    proposal_section = forms.ChoiceField(widget=forms.Select(attrs={'class': 'dropdown'}))
    proposal_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'dropdown'}))

    def __init__(self, conference, *args, **kwargs):
        super(ProposalTypesChoices, self).__init__(*args, **kwargs)
        self.fields['proposal_section'].choices = _get_proposal_section_choices(conference)
        self.fields['proposal_type'].choices = _get_proposal_type_choices(conference)


class ProposalsToReviewForm(ProposalTypesChoices):
    """
    Used to filter proposals
    """
    reviewer_comment = forms.ChoiceField(widget=forms.Select(attrs={'class': 'dropdown'}))

    def __init__(self, conference, *args, **kwargs):
        super(ProposalsToReviewForm, self).__init__(conference, *args, **kwargs)
        self.fields['reviewer_comment'].choices = ProposalReviewerComment.CHOICES


class ProposalVotesFilterForm(ProposalTypesChoices):
    """
    Form  to filter proposals based on votes and review_status.
    """
    votes = forms.ChoiceField(widget=forms.Select(attrs={'class': 'dropdown votes'}))
    review_status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'dropdown'}))

    def __init__(self, conference, *args, **kwargs):
        super(ProposalVotesFilterForm, self).__init__(conference, *args, **kwargs)
        self.fields['votes'].choices = ProposalVotesFilter.CHOICES
        self.fields['review_status'].choices = ProposalReviewStatus.CHOICES

        for name, field in list(self.fields.items()):
            field.choices.insert(0, ('all', 'All'))
