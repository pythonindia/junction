# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Third Party Stuff
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

# Junction Stuff
from junction.tickets.models import Ticket


class Command(BaseCommand):
    """
    Read a csv file containing ticket numbers and
    fill all the details for it.
    """
    @transaction.atomic
    def handle(self, *args, **options):

        if len(args) != 2:
            raise CommandError('Usage: python manage.py fill_data <in_file> <out_file>')

        in_file, out_file = args
        ticket_nums = [line.rstrip('\n') for line in open(in_file).readlines()]

        fh = open(out_file, 'w')
        header = ('Ticket Number', 'Name', 'Email', 'Gender', 'Designation', 'Company', 'City', 'Address')
        fh.write(','.join(header) + '\n')

        for ticket_num in ticket_nums:
            try:
                ticket = Ticket.objects.get(ticket_no=ticket_num)
            except ObjectDoesNotExist:
                print(u"Ticket num: {} not found".format(ticket_num))

            details = ticket.others
            for attendee in details['attendee']:
                if attendee['ticketNo'] == ticket_num:
                    attendee = attendee
                    break
                else:
                    attendee = {}

            if not ticket.address:
                ticket.address = ''

            if not attendee['details']:
                gender = ''
                designation = ''
                city = ''
                company = ''
            else:
                gender = attendee['details']['Gender']
                company = attendee['details']['Company/Organisation']
                designation = attendee['details']['Designation']
                city = attendee['details']['City']

            data = (ticket_num, ticket.name, attendee['email'], gender, designation, company, city, ticket.address)
            fh.write(','.join(data) + '\n')
