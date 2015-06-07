# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0010_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposalsectionreviewervotevalue',
            options={'ordering': ('-vote_value',)},
        ),
    ]
