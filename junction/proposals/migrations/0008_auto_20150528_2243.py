# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0007_auto_20150525_2150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalsectionreviewervote',
            name='up_vote',
        ),
        migrations.AddField(
            model_name='proposalsectionreviewervote',
            name='vote_value',
            field=models.SmallIntegerField(default=True),
            preserve_default=True,
        ),
    ]
