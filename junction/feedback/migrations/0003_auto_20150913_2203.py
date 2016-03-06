# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20150913_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleitemchoicefeedback',
            name='value',
            field=models.SmallIntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='scheduleitemchoicefeedback',
            index_together=set([('schedule_item', 'value'), ('device', 'schedule_item')]),
        ),
    ]
