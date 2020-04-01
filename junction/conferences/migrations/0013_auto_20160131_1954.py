# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("conferences", "0012_historicalconferenceproposalreviewer"),
    ]

    operations = [
        migrations.AddField(
            model_name="conference",
            name="hashtags",
            field=models.CharField(
                max_length=100,
                default="",
                null=True,
                help_text="Used in social sharing, use commas to separate to tags, no '#' required.",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="conference",
            name="twitter_id",
            field=models.CharField(
                max_length=100,
                default="",
                null=True,
                help_text="Used in social share widgets.",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="conference",
            name="venue",
            field=models.ForeignKey(
                blank=True,
                null=True,
                to="conferences.ConferenceVenue",
                on_delete=django.db.models.deletion.CASCADE,
            ),
            preserve_default=True,
        ),
    ]
