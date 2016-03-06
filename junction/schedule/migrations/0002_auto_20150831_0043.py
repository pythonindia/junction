# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleitem',
            name='type',
            field=models.CharField(default=b'TALK', max_length=20, choices=[(b'TALK', b'Talk'), (b'LUNCH', b'Lunch'), (b'BREAK', b'Break'), (b'WORKSHOP', b'Workshop'), (b'POSTER', b'Poster'), (b'OPEN_SPACE', b'Open Space')]),
            preserve_default=True,
        ),
    ]
