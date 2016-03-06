# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0010_auto_20150713_2331'),
        ('proposals', '0012_auto_20150709_0842'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('event_date', models.DateField(db_index=True)),
                ('start_time', models.TimeField(db_index=True)),
                ('end_time', models.TimeField()),
                ('alt_name', models.CharField(max_length=100, blank=True)),
                ('type', models.CharField(default=b'TALK', max_length=20, choices=[(b'TALK', b'Talk'), (b'LUNCH', b'Lunch'), (b'BREAK', b'Break')])),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_scheduleitem_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_scheduleitem_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('room', models.ForeignKey(to='conferences.Room', null=True)),
                ('session', models.ForeignKey(to='proposals.Proposal', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterIndexTogether(
            name='scheduleitem',
            index_together=set([('event_date', 'start_time')]),
        ),
    ]
