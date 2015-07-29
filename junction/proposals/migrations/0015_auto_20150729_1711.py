# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0014_auto_20150728_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproposal',
            name='review_status',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Review Status', choices=[(4, 'On hold'), (3, 'Rejected'), (2, 'Selected'), (5, 'Wait-listed'), (1, 'Yet to be reviewed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproposal',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, choices=[(3, 'Cancelled'), (1, 'Draft'), (2, 'Public')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='historicalproposal',
            name='target_audience',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Target Audience', choices=[(3, 'Advanced'), (1, 'Beginner'), (2, 'Intermediate')]),
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
    ]
