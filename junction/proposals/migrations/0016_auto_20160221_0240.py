# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0015_auto_20150806_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalsection',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proposaltype',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
    ]
