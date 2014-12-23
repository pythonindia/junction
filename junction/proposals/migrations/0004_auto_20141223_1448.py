# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0003_auto_20141223_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='slug',
            field=models.SlugField(default=b''),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='proposal',
            unique_together=set([]),
        ),
    ]
