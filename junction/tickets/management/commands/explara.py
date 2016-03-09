# -*- coding: utf-8 -*-

# Third Party Stuff
import requests


class Explara(object):
    """
    Example Use:
    ea = ExplaraAPI(access_token="xxx")
    tickets = ea.get_tickets(eventid="exxxx")
    """
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {'Authorization': u'Bearer ' + self.access_token}
        self.base_url = 'https://www.explara.com/api/e/{0}'

    def get_events(self):
        events = requests.post(self.base_url.format('get-all-events'), headers=self.headers).json()
        return [{'title': e.get('eventTitle'), 'eventId': e.get('eventId')} for e in events.get('events')]

    def get_ticket_types(self, explara_eventid):
        ticket_types = requests.post(
            self.base_url.format('get-tickets'),
            headers=self.headers,
            data={'eventId': explara_eventid}
        ).json()
        return ticket_types

    def get_orders(self, explara_eventid):
        ticket_orders = []
        completed = False
        from_record = 0
        to_record = 50
        while not completed:
            payload = {
                'eventId': explara_eventid,
                'fromRecord': from_record,
                'toRecord': to_record
            }
            attendee_response = requests.post(
                self.base_url.format('attendee-list'),
                headers=self.headers,
                data=payload
            ).json()
            if not attendee_response.get('attendee'):
                completed = True
            elif isinstance(attendee_response.get('attendee'), list):
                ticket_orders.extend([order for order in attendee_response.get('attendee')])
            # after the first batch, subsequent batches are dicts with batch no. as key.
            elif isinstance(attendee_response.get('attendee'), dict):
                ticket_orders.extend([order for order_idx, order in list(attendee_response.get('attendee').items())])
            print("Synced {} records".format(to_record))
            from_record = to_record
            to_record += 50

        return ticket_orders
