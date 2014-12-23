# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0003_conference_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='slug',
        ),
    ]
