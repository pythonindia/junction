# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicefeedbackquestionvalue',
            name='value',
            field=models.SmallIntegerField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='scheduleitemtextfeedback',
            index_together=set([('device', 'schedule_item')]),
        ),
    ]
