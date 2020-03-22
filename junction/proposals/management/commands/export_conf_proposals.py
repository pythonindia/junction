
import io
from os.path import join
from settings.common import ROOT_DIR

from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from xlsxwriter.workbook import Workbook

from junction.conferences.models import Conference
from junction.proposals.models import (
    Proposal,
    ProposalComment,
    ProposalSectionReviewer,
    ProposalSectionReviewerVoteValue,
    )
from junction.base.constants import (
    ProposalReviewVote,
    ProposalStatus,
    ProposalReviewStatus,
    )

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--conference_slug', default=None, help='Enter the conference slug where to export reviewer votes from')

        parser.add_argument('--user_id', default=None, help='Enter your user id')

    def handle(self, *args, **options):

        conference = get_object_or_404(Conference, slug=self.options.get('conference_slug'))
        user = User.objects.get(id=self.options.get('user_id'))

        if not conference_is_moderator(user=user, conference=conference):
            raise PermissionDenied

        proposal_sections = conference.proposal_sections.all()
        proposals_qs = Proposal.objects.select_related('proposal_type', 'proposal_section', 'conference', 'author').filter(conference=conference, status=ProposalStatus.PUBLIC)
        proposals_qs = sorted(proposals_qs, key=lambda x: x.get_reviewer_votes_sum(), reverse=True)
        vote_values_list = ProposalSectionReviewerVoteValue.objects.order_by('-vote_value')
        vote_values_list = [v.vote_value for v in vote_values_list]
        vote_values_desc = tuple(i.description for i in ProposalSectionReviewerVoteValue.objects.order_by('-vote_value'))
        header = ('Proposal Type', 'Title', 'Sum of reviewer votes', 'No. of reviewer votes') + tuple(vote_values_desc) + ('Public votes count', 'Vote comments')
        output = io.BytesIO()

        with Workbook(output) as book:
            for section in proposal_sections:
                sheet = book.add_worksheet(section.name[:30])
                cell_format = book.add_format({'bold': True})
                sheet.write_row(0, 0, header, cell_format)

                section_proposals = [p for p in proposal_qs if p.proposal_section == section]

                for index, p in enumerate(section_proposals, 1):
                    vote_details = tuple(p.get_reviewer_votes_count_by_value(v) for v in vote_values_list)
                    vote_comment = '\n'.join([comment.comment for comment in p.proposalcomment_set.filter(vote=True, deleted=False)])
                    row = (p.proposal_type.name, p.title, p.get_reviewer_votes_sum(), p.get_reviewer_votes_count(),) + vote_details + (p.get_voutes_count(), vote_comment,)
                    if p.get_reviewer_votes_count_by_value(ProposalSectionReviewerVoteValue.objects.get(vote_value=ProposalReviewVote.NOT_ALLOWED).vote_value) > 0:
                        cell_format = book.add_format({'bg_color': 'red'})
                    elif p.get_reviewer_votes_count_by_value(ProposalSectionReviewerVoteValue.objects.get(vote_value=ProposalReviewVote.MUST_HAVE).vote_value) > 2:
                        cell_format = book.add_format({'bg_color': 'red'})
                    elif p.get_reviewer_votes_count() < 2:
                        cell_format = book.add_format({'bg_color': 'yellow'})
                    else:
                        cell_format = None

                    sheet.write_row(index, 0, row, cell_format)

        output.seek(0)

        excel_file_name = "%s-%s" % (user.name, conference.name)
        excel_file_location = join(ROOT_DIR, 'excels', excel_file_name)

        with open(excel_file_location, 'wb') as excelfile:
            excelfile.write(output.read())

        self.stdout.write("Successfully created the excel file")
