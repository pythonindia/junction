import tablib
from django.core.management.base import BaseCommand, CommandError
from junction.conferences.models import Conference
from junction.proposals.models import Proposal


class Command(BaseCommand):
    help = "Generate a CSV file of all proposers for a conference."

    def add_arguments(self, parser):
        parser.add_argument('conference_slug', nargs=1, type=str)

    def has_conference(self, slug):
        try:
            conference = Conference.objects.get(slug=slug)
            return conference
        except Conference.DoesNotExist:
            raise CommandError('Conference "{}" does not exist'.format(slug))

    def handle(self, *args, **kwargs):
        conference_slug = kwargs['conference_slug'][0]
        conference = self.has_conference(slug=conference_slug)
        proposers_file = tablib.Dataset()
        proposers_file.headers = [
            'Name', 'Email', 'Title', 'Type', 'Section']

        for proposal in Proposal.objects.filter(
                conference_id=conference.id):
            proposers_file.append([proposal.author.username,
                                   proposal.author.email,
                                   proposal.title,
                                   proposal.proposal_type,
                                   proposal.proposal_section])

        with open('{}.csv'.format(conference_slug), 'w') as f:
            f.write(proposers_file.csv)

        self.stdout.write(self.style.SUCCESS(
            'Successfully created CSV file: "%s.csv"' % conference_slug))
