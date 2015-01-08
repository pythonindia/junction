# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_auto_20141223_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(populate_from=(b'title',), max_length=255, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='proposal',
            unique_together=set([('conference', 'slug')]),
        ),
    ]
