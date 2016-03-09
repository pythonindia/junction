# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_auto_20150917_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleitem',
            name='session',
            field=models.ForeignKey(blank=True, to='proposals.Proposal', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scheduleitem',
            name='type',
            field=models.CharField(default=b'Talk', max_length=20, choices=[(b'Talk', b'Talk'), (b'Lunch', b'Lunch'), (b'Break', b'Break'), (b'Workshop', b'Workshop'), (b'Poster', b'Poster'), (b'Open Space', b'Open Space'), (b'Introduction', b'Introduction'), (b'Lightning Talk', b'Lightning Talk')]),
            preserve_default=True,
        ),
    ]
