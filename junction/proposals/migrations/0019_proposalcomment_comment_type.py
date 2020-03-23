# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("proposals", "0018_auto_20160806_1727"),
    ]

    operations = [
        migrations.AddField(
            model_name="proposalcomment",
            name="comment_type",
            field=models.PositiveSmallIntegerField(
                default=0,
                choices=[(0, "All general comments"), (1, "Second phase voting")],
            ),
            preserve_default=True,
        ),
    ]
