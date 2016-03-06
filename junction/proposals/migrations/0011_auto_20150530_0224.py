# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


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
