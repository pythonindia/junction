# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Standard Library
import datetime

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0013_proposalcomment_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalsection',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='proposalsection',
            name='start_date',
        ),
        migrations.AddField(
            model_name='proposaltype',
            name='end_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='End Date'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposaltype',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Start Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='review_status',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Review Status', choices=[(4, 'On hold'), (3, 'Rejected'), (2, 'Selected'), (5, 'Wait-listed'), (1, 'Yet to be reviewed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, choices=[(3, 'Cancelled'), (1, 'Draft'), (2, 'Public')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='target_audience',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Target Audience', choices=[(3, 'Advanced'), (1, 'Beginner'), (2, 'Intermediate')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalcomment',
            name='vote',
            field=models.BooleanField(default=False, verbose_name='What is the reason?'),
            preserve_default=True,
        ),
    ]
