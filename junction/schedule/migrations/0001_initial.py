# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0011_auto_20150530_0224'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0010_auto_20150713_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('event_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('alt_name', models.CharField(max_length=100, blank=True)),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_scheduleitem_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_scheduleitem_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('room', models.ForeignKey(to='conferences.Room', null=True)),
                ('session', models.ForeignKey(to='proposals.Proposal', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
