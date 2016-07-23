import collections

from junction.base.constants import ProposalReviewVote, ProposalVotesFilter
from junction.proposals.models import ProposalSection


def _sort_proposals_for_dashboard(conference, proposals_qs, user, form):
    """
    """
    cps = form.cleaned_data['proposal_section']
    cpt = form.cleaned_data['proposal_type']
    votes = form.cleaned_data['votes']
    review_status = form.cleaned_data['review_status']

    proposal_sections = conference.proposal_sections.all()
    s_items = collections.namedtuple('section_items', 'section proposals')
    proposals = []

    if cps != 'all':
        proposal_sections = ProposalSection.objects.filter(pk=cps)
    if cpt != 'all':
        proposals_qs = proposals_qs.filter(proposal_type__id__in=cpt)
    if votes != 'all':
        votes = int(votes)
    if review_status != 'all':
        proposals_qs = proposals_qs.filter(review_status=review_status)

    if votes == ProposalVotesFilter.NO_VOTES:
        proposals_qs = [
            p for p in proposals_qs if p.get_reviewer_votes_count() == votes]
    elif votes == ProposalVotesFilter.MIN_ONE_VOTE:
        proposals_qs = [
            p for p in proposals_qs if p.get_reviewer_votes_count() >= votes]
    elif votes == ProposalVotesFilter.SORT_BY_REVIEWER:
        proposals_qs = sorted(
            proposals_qs,
            key=lambda x: x.get_reviewer_vote_value(reviewer=user),
            reverse=True,
        )
    elif votes == ProposalVotesFilter.SORT_BY_SUM:
        proposals_qs = sorted(
            proposals_qs, key=lambda x: x.get_reviewer_votes_sum(),
            reverse=True)
        proposals = [s_items('', proposals_qs)]

    elif votes == ProposalVotesFilter.SORT_BY_SELECTION:
        # Selection of proposal is based on conference guidelines.
        # More info is available at http://tiny.cc/qzo5cy

        proposals_qs = [p for p in proposals_qs if not p.has_negative_votes()]
        proposals_qs = sorted(proposals_qs, key=lambda x: x.get_reviewer_votes_sum(), reverse=True)

        selected = [p for p in proposals_qs if p.get_reviewer_votes_count_by_value(ProposalReviewVote.MUST_HAVE) > 1]
        proposals.append(s_items('Selected', selected))

        batches = []

        batch1 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.MUST_HAVE) > 0 and
                  p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) > 1]
        proposals.append(s_items('Batch 1', batch1))
        batches += batch1

        batch2 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.MUST_HAVE) > 0 and
                  p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) > 0 and
                  p not in batches]
        proposals.append(s_items('Batch 2', batch2))
        batches += batch2

        batch3 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) > 1 and
                  p not in batches]
        proposals.append(s_items('Batch 3', batch3))
        batches += batch3

        batch4 = [p for p in proposals_qs
                  if p.get_reviewer_votes_count_by_value(ProposalReviewVote.GOOD) > 0 and
                  p.get_reviewer_votes_count_by_value(ProposalReviewVote.NOT_BAD) > 1 and
                  p not in batches]
        proposals.append(s_items('Batch 4', batch4))

        # proposals = selected + batch1 + batch2 + batch3 + batch4
        # unique_proposals = set()
        # proposals = [x for x in proposals if not (x in unique_proposals or unique_proposals.add(x))]
        # proposals = [s_items('', set(proposals))]

    if votes not in (ProposalVotesFilter.SORT_BY_SUM, ProposalVotesFilter.SORT_BY_SELECTION):
        print('f')
        for section in proposal_sections:
            section_proposals = [p for p in proposals_qs if p.proposal_section == section]
            proposals.append(s_items(section, section_proposals))

    return proposals
