# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid_upload_path.storage
from django.db import migrations, models


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
