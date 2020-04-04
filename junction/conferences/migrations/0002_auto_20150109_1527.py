# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conferencemoderator',
            options={'verbose_name': 'moderator', 'verbose_name_plural': 'moderators'},
        ),
        migrations.AlterModelOptions(
            name='conferenceproposalreviewer',
            options={'verbose_name': 'proposals reviewer', 'verbose_name_plural': 'proposals reviewers'},
        ),
        migrations.AlterField(
            model_name='conferencemoderator',
            name='conference',
            field=models.ForeignKey(related_name='moderators', to='conferences.Conference', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conferenceproposalreviewer',
            name='conference',
            field=models.ForeignKey(related_name='proposal_reviewers', to='conferences.Conference', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='conferencemoderator',
            unique_together=set([('conference', 'moderator')]),
        ),
    ]
