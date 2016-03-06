# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0012_historicalconferenceproposalreviewer'),
        ('schedule', '0003_scheduleitemtype'),
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChoiceFeedbackQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('is_required', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, verbose_name='Choice Feedback Title')),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('schedule_item_type', models.ForeignKey(to='schedule.ScheduleItemType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChoiceFeedbackQuestionValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('title', models.CharField(max_length=255, verbose_name='Choice Feedback Value Title')),
                ('value', models.SmallIntegerField()),
                ('question', models.ForeignKey(related_name='allowed_values', to='feedback.ChoiceFeedbackQuestion')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScheduleItemChoiceFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('value', models.SmallIntegerField()),
                ('device', models.ForeignKey(blank=True, to='devices.Device', null=True)),
                ('question', models.ForeignKey(to='feedback.ChoiceFeedbackQuestion')),
                ('schedule_item', models.ForeignKey(to='schedule.ScheduleItem')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ScheduleItemTextFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('text', models.TextField()),
                ('device', models.ForeignKey(blank=True, to='devices.Device', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextFeedbackQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('is_required', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, verbose_name='Text Feedback Title')),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('schedule_item_type', models.ForeignKey(to='schedule.ScheduleItemType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scheduleitemtextfeedback',
            name='question',
            field=models.ForeignKey(to='feedback.TextFeedbackQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scheduleitemtextfeedback',
            name='schedule_item',
            field=models.ForeignKey(to='schedule.ScheduleItem'),
            preserve_default=True,
        ),
    ]
