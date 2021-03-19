# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-10 13:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("proposals", "0023_auto_20170610_1633"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="spamcomment",
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name="spamcomment",
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name="spamcomment",
            name="comment",
        ),
        migrations.RemoveField(
            model_name="spamcomment",
            name="marked_by",
        ),
        migrations.AddField(
            model_name="proposalcomment",
            name="marked_as_spam_by",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="marked_as_spam_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterIndexTogether(
            name="proposalcomment",
            index_together=set([("is_spam", "marked_as_spam_by")]),
        ),
        migrations.DeleteModel(
            name="SpamComment",
        ),
    ]
