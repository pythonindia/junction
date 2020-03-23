# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("proposals", "0005_proposalsectionreviewer_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proposal",
            name="content_urls",
            field=models.TextField(default="", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="proposal",
            name="prerequisites",
            field=models.TextField(default="", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="proposal",
            name="review_status",
            field=models.PositiveSmallIntegerField(
                default=1,
                verbose_name="Review Status",
                choices=[
                    (1, "Yet to be reviewed"),
                    (2, "Selected"),
                    (3, "Rejected"),
                    (4, "On hold"),
                    (5, "Wait-listed"),
                ],
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="proposal",
            name="speaker_info",
            field=models.TextField(default="", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="proposal",
            name="speaker_links",
            field=models.TextField(default="", blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="proposal",
            name="status",
            field=models.PositiveSmallIntegerField(
                default=1, choices=[(2, "Public"), (1, "Draft"), (3, "Cancelled")]
            ),
            preserve_default=True,
        ),
    ]
