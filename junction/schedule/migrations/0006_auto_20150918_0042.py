# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_auto_20150917_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduleitem',
            name='alt_description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scheduleitem',
            name='alt_name',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
