# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_proposalsectionreviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalsectionreviewer',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Is Active?'),
            preserve_default=True,
        ),
    ]
