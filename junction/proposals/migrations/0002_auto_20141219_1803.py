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
            name='target_audience',
            field=models.CharField(default=b'Beginner', max_length=255, verbose_name=b'Target Audience', choices=[(b'0', b'Beginner'), (b'1', b'Intermediate'), (b'2', b'Advanced')]),
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
            field=models.CharField(default=b'Yet to be reviewed', max_length=255, verbose_name=b'Review Status', choices=[(b'0', b'Yet to be reviewed'), (b'1', b'Selected'), (b'2', b'Rejected'), (b'3', b' On hold'), (b'4', b'Wait-listed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(default=b'Draft', max_length=255, choices=[(b'0', b'Draft'), (b'1', b'Public'), (b'2', b'Cancelled')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalcomment',
            name='visibility',
            field=models.CharField(default=b'Public', max_length=255, choices=[(b'0', b'Public'), (b'1', b'Private')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposalvote',
            name='role',
            field=models.CharField(default=b'Public', max_length=255, choices=[(b'0', b'Public'), (b'1', b'Reviewer')]),
            preserve_default=True,
        ),
    ]
