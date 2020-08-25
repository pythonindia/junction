# -*- coding: utf-8 -*-
import csv
import os
import sys

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from settings.common import ROOT_DIR

from junction.base.constants import ProposalStatus
from junction.conferences.models import Conference
from junction.proposals.models import Proposal, ProposalSectionReviewerVoteValue
from junction.proposals.permissions import is_conference_moderator


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--conference_slug",
            default=None,
            help="Enter the conference whose reviewer votes are to be exported from",
        )

        parser.add_argument("--user_id", default=None, help="Enter your user id")

    def handle(self, *args, **options):

        try:
            conference = Conference.objects.get(slug=options.get("conference_slug"))
            user = User.objects.get(id=options.get("user_id"))
        except User.DoesNotExist:
            self.stdout.write("Invalid user")
            sys.exit(1)
        except Conference.DoesNotExist:
            self.stdout.write("Invalid conference")
            sys.exit(1)

        if not is_conference_moderator(user=user, conference=conference):
            self.stdout.write("The user id is not a conference moderator")
            sys.exit(1)

        proposal_sections = conference.proposal_sections.all()
        proposals_qs = Proposal.objects.select_related(
            "proposal_type", "proposal_section", "conference", "author"
        ).filter(conference=conference, status=ProposalStatus.PUBLIC)
        proposals_qs = sorted(
            proposals_qs, key=lambda x: x.get_reviewer_votes_sum(), reverse=True
        )
        proposal_vote_values = ProposalSectionReviewerVoteValue.objects.order_by(
            "-vote_value"
        )
        vote_values_list = [v.vote_value for v in proposal_vote_values]
        vote_values_desc = tuple(i.description for i in proposal_vote_values)
        header = ("Proposal Type", "Title", "Sum of reviewer votes", "No. of reviewer votes")
            + ("Public votes count", "Vote comments")
            + tuple(vote_values_desc)

        csv_contents = []

        for section in proposal_sections:
            section_proposals = [
                p for p in proposals_qs if p.proposal_section == section
            ]

            for index, p in enumerate(section_proposals, 1):
                vote_details = tuple(
                    p.get_reviewer_votes_count_by_value(v) for v in vote_values_list
                )
                vote_comment = "\n".join(
                    [
                        comment.comment
                        for comment in p.proposalcomment_set.filter(
                            vote=True, deleted=False
                        )
                    ]
                )
                row = {
                    header[0]: p.proposal_type.name,
                    header[1]: p.title,
                    header[2]: p.get_reviewer_votes_sum(),
                    header[3]: p.get_reviewer_votes_count(),
                    header[4]: p.get_votes_count(),
                    header[5]: vote_comment,
                }
                for i in range(len(tuple(vote_values_desc))):
                    row[tuple(vote_values_desc)[i]] = vote_details[i]

                csv_contents.append(row)

        csv_file_name = "%s-%s.csv" % (user.username, conference.name)
        csv_base_dir = os.path.join(ROOT_DIR, "csvs")

        if not os.path.exists(csv_base_dir):
            os.makedirs(csv_base_dir)

        csv_file_location = os.path.join(ROOT_DIR, "csvs", csv_file_name)

        with open(csv_file_location, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)

            writer.writeheader()
            for row in csv_contents:
                writer.writerow(row)

        self.stdout.write("Successfully created the csv file")
