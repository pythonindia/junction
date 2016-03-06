# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_scheduleitemtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleitem',
            name='type',
            field=models.CharField(default=b'Talk', max_length=20, choices=[(b'Talk', b'Talk'), (b'Lunch', b'Lunch'), (b'Break', b'Break'), (b'Workshop', b'Workshop'), (b'Poster', b'Poster'), (b'Open Space', b'Open Space'), (b'Introduction', b'Introduction')]),
            preserve_default=True,
        ),
    ]
