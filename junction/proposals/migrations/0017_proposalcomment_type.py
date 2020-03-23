# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("proposals", "0016_auto_20160221_0240"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposalcomment",
            name="type",
            field=models.PositiveSmallIntegerField(
                default=0, choices=[(0, "Unclassified"), (1, "Second phase voting")]
            ),
            preserve_default=True,
        ),
    ]
