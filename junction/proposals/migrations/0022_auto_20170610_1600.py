# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-10 10:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("proposals", "0021_auto_20160905_0044"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpamComment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
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
            ],
        ),
        migrations.AddField(
            model_name="proposalcomment",
            name="is_spam",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="spamcomment",
            name="comment",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to="proposals.ProposalComment",
            ),
        ),
        migrations.AddField(
            model_name="spamcomment",
            name="marked_by",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterUniqueTogether(
            name="spamcomment",
            unique_together=set([("comment", "marked_by")]),
        ),
    ]
