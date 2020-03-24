# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0017_proposalcomment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalcomment',
            name='type',
        ),
        migrations.AddField(
            model_name='historicalproposalsectionreviewervote',
            name='phase',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Initial voting'), (1, 'Second phase voting')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposalsectionreviewervote',
            name='phase',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Initial voting'), (1, 'Second phase voting')]),
            preserve_default=True,
        ),
    ]
