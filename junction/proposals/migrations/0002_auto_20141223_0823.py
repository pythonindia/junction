# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='target_audienance',
        ),
        migrations.AddField(
            model_name='proposal',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name=b'Is Deleted?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='slug',
            field=models.SlugField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='target_audience',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'Target Audience', choices=[(1, b'Beginner'), (2, b'Intermediate'), (3, b'Advanced')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposalcomment',
            name='deleted',
            field=models.BooleanField(default=False, verbose_name=b'Is Deleted?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='review_status',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'Review Status', choices=[(1, b'Yet to be reviewed'), (2, b'Selected'), (3, b'Rejected'), (4, b' On hold'), (5, b'Wait-listed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, b'Draft'), (2, b'Public'), (3, b'Cancelled')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalcomment',
            name='visibility',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, b'Public'), (2, b'Private')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalvote',
            name='role',
            field=models.PositiveSmallIntegerField(default=1, choices=[(1, b'Public'), (2, b'Reviewer')]),
            preserve_default=True,
        ),
    ]
