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
            field=models.CharField(max_length=255, verbose_name=b'Current Status', choices=[(b'0', b'Accepting Call for Proposals'), (b'1', b'Closed for Proposals'), (b'2', b'Accepting Votes'), (b'3', b'Schedule Published')]),
            preserve_default=True,
        ),
    ]
