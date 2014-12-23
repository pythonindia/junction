# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0002_auto_20141223_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(default='', populate_from=(b'name',), editable=False, max_length=255, blank=True, unique=True),
            preserve_default=False,
        ),
    ]
