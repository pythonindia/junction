# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conferences", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="conferencemoderator",
            options={"verbose_name": "moderator", "verbose_name_plural": "moderators"},
        ),
        migrations.AlterModelOptions(
            name="conferenceproposalreviewer",
            options={
                "verbose_name": "proposals reviewer",
                "verbose_name_plural": "proposals reviewers",
            },
        ),
        migrations.AlterField(
            model_name="conferencemoderator",
            name="conference",
            field=models.ForeignKey(
                related_name="moderators", to="conferences.Conference"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="conferenceproposalreviewer",
            name="conference",
            field=models.ForeignKey(
                related_name="proposal_reviewers", to="conferences.Conference"
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="conferencemoderator",
            unique_together=set([("conference", "moderator")]),
        ),
    ]
