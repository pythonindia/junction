# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import junction.devices.models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='verification_code_expires_at',
            field=models.DateTimeField(default=junction.devices.models.expiry_time, verbose_name='Verification Code Expires At'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='verification_code_sent_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Verification Code Sent At'),
            preserve_default=True,
        ),
    ]
