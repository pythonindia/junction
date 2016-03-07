# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

# Standard Library
from datetime import date

# Third Party Stuff
import arrow
from django import template

register = template.Library()


@register.filter
def fromnow(value):
    """
    A wrapper around arrow.humanize(), returns natural time which is less precise than
    django's naturaltime filter. It doesn't display weeks and combination of days & hours.
    """
    if not (isinstance(value, date) or isinstance(value, arrow.Arrow)):  # datetime is a subclass of date
        return value

    return arrow.get(value).humanize()
