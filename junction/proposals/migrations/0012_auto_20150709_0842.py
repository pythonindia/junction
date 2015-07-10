# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0011_auto_20150530_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalsection',
            name='end_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='End Date'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposalsection',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Start Date'),
            preserve_default=True,
        ),
    ]
