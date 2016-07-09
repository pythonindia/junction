# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0003_auto_20160706_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 9, 14, 52, 47, 54125, tzinfo=utc), verbose_name='Created At', auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='created_by',
            field=models.ForeignKey(related_name='created_profile_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='modified_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 9, 14, 53, 1, 840388, tzinfo=utc), verbose_name='Last Modified At', auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='modified_by',
            field=models.ForeignKey(related_name='updated_profile_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
