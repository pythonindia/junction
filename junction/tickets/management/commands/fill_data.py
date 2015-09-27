# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Third Party Stuff
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
        header = ','.join(('ticket_num', 'name', 'email', 'address', '\n'))
        fh.write(header)

        for ticket_num in ticket_nums:
            ticket = Ticket.objects.get(ticket_no=ticket_num)

            details = ticket.others
            for attendee in details['attendee']:
                if attendee['ticketNo'] == ticket_num:
                    attendee = attendee
                    break
                else:
                    attendee = {}

            if not ticket.address:
                ticket.address = ''
            data = data = ','.join((ticket_num, ticket.name, attendee['email'], ticket.address, '\n'))
            fh.write(data)
