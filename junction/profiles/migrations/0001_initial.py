# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("city", models.CharField(max_length=100, null=True, blank=True)),
                ("contact_no", models.CharField(max_length=15, null=True, blank=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="created_profile_set",
                        verbose_name="Created By",
                        blank=True,
                        on_delete=models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        related_name="updated_profile_set",
                        verbose_name="Modified By",
                        blank=True,
                        on_delete=models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.deletion.CASCADE,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=(models.Model,),
        ),
    ]
