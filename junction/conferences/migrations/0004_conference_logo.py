# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid_upload_path.storage


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0003_auto_20150113_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=uuid_upload_path.storage.upload_to),
            preserve_default=True,
        ),
    ]
