# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_auto_20150416_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalcomment',
            name='reviewer',
            field=models.BooleanField(default=False, verbose_name='Is Reviewer?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='target_audience',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Target Audience', choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalvote',
            name='role',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, 'Public'), (2, 'Reviewer')]),
            preserve_default=True,
        ),
    ]
