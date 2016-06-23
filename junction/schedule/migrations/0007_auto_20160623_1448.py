# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20150918_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleitem',
            name='type',
            field=models.CharField(max_length=20, default='Talk', choices=[('Talk', 'Talk'), ('Lunch', 'Lunch'), ('Break', 'Break'), ('Workshop', 'Workshop'), ('Poster', 'Poster'), ('Open Space', 'Open Space'), ('Introduction', 'Introduction'), ('Lightning Talk', 'Lightning Talk')]),
            preserve_default=True,
        ),
    ]
