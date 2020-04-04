# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("proposals", "0019_proposalcomment_comment_type"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="proposalsectionreviewervote", unique_together=set([]),
        ),
    ]
