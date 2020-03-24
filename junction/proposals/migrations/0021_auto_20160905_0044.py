# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0020_auto_20160806_2023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proposalcomment',
            options={'ordering': ('created_at',)},
        ),
    ]
