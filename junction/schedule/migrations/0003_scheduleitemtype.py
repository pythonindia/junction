# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.conf import settings
from django.db import migrations, models

SCHEDULE_ITEM_TYPES = ['Talk', 'Lunch', 'Break', 'Workshop',
                       'Poster', 'Open Space']


def load_fixture(apps, schema_editor):
    Model = apps.get_model("schedule", "ScheduleItemType")
    for item_type in SCHEDULE_ITEM_TYPES:
        Model.objects.create(title=item_type)


def unload_fixture(apps, schema_editor):
    Model = apps.get_model("schedule", "ScheduleItemType")
    for item_type in SCHEDULE_ITEM_TYPES:
        for obj in Model.objects.filter(title=item_type):
            obj.delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0002_auto_20150831_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleItemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('title', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(related_name='created_scheduleitemtype_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_scheduleitemtype_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(load_fixture, reverse_code=unload_fixture)
    ]
