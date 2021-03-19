# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conferences", "0001_initial"),
        ("proposals", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="conferenceproposalsection",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="conferenceproposalsection",
            name="conference",
        ),
        migrations.RemoveField(
            model_name="conferenceproposalsection",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="conferenceproposalsection",
            name="modified_by",
        ),
        migrations.RemoveField(
            model_name="conferenceproposalsection",
            name="proposal_section",
        ),
        migrations.DeleteModel(
            name="ConferenceProposalSection",
        ),
        migrations.AlterUniqueTogether(
            name="conferenceproposaltype",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="conferenceproposaltype",
            name="conference",
        ),
        migrations.RemoveField(
            model_name="conferenceproposaltype",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="conferenceproposaltype",
            name="modified_by",
        ),
        migrations.RemoveField(
            model_name="conferenceproposaltype",
            name="proposal_type",
        ),
        migrations.DeleteModel(
            name="ConferenceProposalType",
        ),
        migrations.AddField(
            model_name="proposalsection",
            name="conferences",
            field=models.ManyToManyField(to="conferences.Conference"),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="proposaltype",
            name="conferences",
            field=models.ManyToManyField(to="conferences.Conference"),
            preserve_default=True,
        ),
    ]
