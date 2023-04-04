import pytest
from unittest.mock import MagicMock

from junction.tickets.management.commands.explara import Explara
from junction.tickets.management.commands.sync_data import Command


def none_events():
    return None


def single_event():
    return [{"eventId": "EKDJHH", "eventTitle ": "My Demo Event"}]


def none_order():
    return None


def single_order():
    order = {
        "orderNo": "E4CACBXXXXX528384A20C930",
        "orderCost": "127.19",
        "quantity": "2",
        "status": "success",
        "paidBy": "online",
        "paidTo": None,
        "refundAmount": None,
        "purchaseDate": "2013-11-13",
        "name": "Pankaj Kumar",
        "email": "dummy@mydummydomain.com",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "address": "address",
        "zipcode": "411027",
        "phoneNo": "22222",
        "attendee": [
            {
                "ticketName": "Free Visit",
                "ticketId": "TKEFAJC",
                "name": "Pankaj Kumar",
                "email": "dummy@mydummydomain.com",
                "checkin": "no",
                "ticketNo": "E4CACB-694",
                "status": "attending",
                "details": {"Date": ""},
            }
        ],
    }
    return [order]


def single_order_no_ticketId():
    order = single_order()
    if "ticketId" in order[0]["attendee"]:
        del order[0]["attendee"]["ticketId"]
    return order


def single_order_no_attendee():
    order = single_order()
    if "attendee" in order[0]:
        del order[0]["attendee"]
    return order


def command_case(get_event_method, get_order_method):
    c = Command()
    e = Explara("ahjbladjsbfafdkjsldkl")
    e.get_events = MagicMock(return_value=get_event_method())
    e.get_orders = MagicMock(return_value=get_order_method())
    c.set_explara(e)
    c.handle()


@pytest.mark.django_db(transaction=True)
def test_suite_command():
    with pytest.raises(TypeError):
        command_case(none_events, none_order)
    with pytest.raises(TypeError):
        command_case(single_event, none_order)
    command_case(single_event, single_order)
    command_case(single_event, single_order_no_ticketId)
    command_case(single_event, single_order_no_attendee)
