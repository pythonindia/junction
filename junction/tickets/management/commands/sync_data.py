# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

# Third Party Stuff
import qrcode
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

# Junction Stuff
from junction.tickets.models import Ticket

from .explara import Explara
import os


class Command(BaseCommand):
    """
    Sync tickets info from explara and
    generate QR codes for each ticket.
    """

    def __init__(self, api_token=settings.EXPLARA_API_TOKEN):
        self.explara = Explara(api_token)

    def set_explara(self, explara):
        self.explara = explara

    def handle(self, *args, **options):
        events = self.explara.get_events()
        orders = self.explara.get_orders(events[0]['eventId'])
        if not os.path.isdir(settings.QR_CODES_DIR):
            os.makedirs(settings.QR_CODES_DIR)
        for order in orders:
            for attendee in order.get('attendee', []):
                ticket_no = attendee.get('ticketId')
                defaults = {
                    'order_no': order.get('orderNo'),
                    'order_cost': order.get('orderCost'),
                    'address': order.get('address', None),
                    'city': order.get('city', None),
                    'zipcode': order.get('zipcode', None),
                    'name': attendee.get('name'),
                    'email': attendee.get('email') or order.get('email'),
                    'status': attendee.get('status'),
                    'others': order,
                }
                with transaction.atomic():
                    ticket, created = Ticket.objects.update_or_create(
                        ticket_no=ticket_no,
                        defaults=defaults
                    )

                if created:
                    qr_code = qrcode.make(ticket_no)
                    file_name = attendee.get('name') + '_' + ticket_no
                    qr_code.save(
                        '{}/{}.png'.format(settings.QR_CODES_DIR, file_name))
