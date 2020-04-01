# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("proposals", "0002_auto_20150105_2220"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proposalsection",
            name="conferences",
            field=models.ManyToManyField(
                to="conferences.Conference", related_name="proposal_sections"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="proposaltype",
            name="conferences",
            field=models.ManyToManyField(
                to="conferences.Conference", related_name="proposal_types"
            ),
            preserve_default=True,
        ),
    ]
