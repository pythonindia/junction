# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import junction.devices.models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(
                        unique=True, max_length=32, db_index=True
                    ),
                ),
                ("is_verified", models.BooleanField(default=False)),
                ("verification_code", models.IntegerField()),
                (
                    "verification_code_sent_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name=b"Verification Code Sent At"
                    ),
                ),
                (
                    "verification_code_expires_at",
                    models.DateTimeField(
                        default=junction.devices.models.expiry_time,
                        verbose_name=b"Verification Code Expires At",
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
    ]
