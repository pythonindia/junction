# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencemoderator',
            name='conference',
            field=models.ForeignKey(to='conferences.Conference', related_name='moderators'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conferenceproposalreviewer',
            name='conference',
            field=models.ForeignKey(to='conferences.Conference', related_name='proposal_reviewers'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='conferencemoderator',
            unique_together=set([('conference', 'moderator')]),
        ),
    ]
