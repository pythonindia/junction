# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

# Third Party Stuff
from celery import shared_task


@shared_task
def add(x, y):
    # dummy task
    print(x + y)
