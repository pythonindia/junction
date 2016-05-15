from junction.tickets.management.commands.sync_data import Command
from junction.tickets.management.commands.explara import Explara
from mock import MagicMock
import pytest


def none_events():
    return None


def single_event():
    list_of_event = list()
    list_of_event.append(
        {"eventId": "EKDJHH", "eventTitle ": "My Demo Event", })
    return list_of_event


def none_order():
    return None


def single_order():
    order = dict()
    order["orderNo"] = "E4CACBXXXXX528384A20C930"
    order["orderCost"] = "127.19"
    order["quantity"] = "2"
    order["status"] = "success"
    order["paidBy"] = "online"
    order["paidTo"] = None
    order["refundAmount"] = None
    order["purchaseDate"] = "2013-11-13"
    order["name"] = "PankajKumar"
    order["email"] = "dummy@mydummydomain.com"
    order["city"] = "Pune"
    order["state"] = "Maharashtra"
    order["country"] = "India"
    order["address"] = "address"
    order["zipcode"] = "411027"
    order["phoneNo"] = "22222"
    order["attendee"] = [{"ticketName": "Free Visit",
                          "ticketId": "TKEFAJC",
                          "name": "Pankaj Kumar",
                          "email": "dummy@mydummydomain.com",
                          "checkin": "no",
                          "ticketNo": "E4CACB-694",
                          "status": "attending",
                          "details": {"Date": ""}}]
    list_of_order = list()
    list_of_order.append(order)
    return list_of_order


def single_order_no_ticketId():
    order = single_order()
    if "ticketId" in order[0]["attendee"]:
        del order[0]["attendee"]["ticketId"]
    return order


def single_order_no_attendee():
    order = single_order()
    if 'attendee' in order[0]:
        del order[0]['attendee']
    return order


def command_case(get_event_method, get_order_method):
    c = Command()
    e = Explara('ahjbladjsbfafdkjsldkl')
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
