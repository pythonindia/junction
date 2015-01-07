# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name=b'Is Deleted?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name=b'Current Status', choices=[(1, b'Accepting Call for Proposals'), (2, b'Closed for Proposals'), (3, b'Accepting Votes'), (4, b'Schedule Published')]),
            preserve_default=True,
        ),
    ]
