# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.conf import settings
from django.db import migrations, models

# Junction Stuff
from junction.base.constants import ConferenceSettingConstants


def add_default_values(apps, schema_editor):
    """Add all default values
    """
    ConferenceSetting = apps.get_model("conferences", "ConferenceSetting")
    public_voting = ConferenceSettingConstants.ALLOW_PUBLIC_VOTING_ON_PROPOSALS
    display_propsals = ConferenceSettingConstants.DISPLAY_PROPOSALS_IN_PUBLIC
    allow_plus_zero_vote = ConferenceSettingConstants.ALLOW_PLUS_ZERO_REVIEWER_VOTE

    Conference = apps.get_model("conferences", "Conference")
    for conf in Conference.objects.all():
        ConferenceSetting.objects.create(
            name=public_voting['name'],
            value=public_voting['value'],
            description=public_voting['description'],
            conference=conf)
        ConferenceSetting.objects.create(
            name=display_propsals['name'],
            value=display_propsals['value'],
            description=display_propsals['description'],
            conference=conf)
        ConferenceSetting.objects.create(
            name=allow_plus_zero_vote['name'],
            value=allow_plus_zero_vote['value'],
            description=allow_plus_zero_vote['description'],
            conference=conf)


def remove_default_values(apps, schema_editor):
    ConferenceSetting = apps.get_model("conferences", "ConferenceSetting")
    objs = ConferenceSetting.objects.all()
    for obj in objs:
        obj.delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0013_auto_20160131_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('value', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255)),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_conferencesetting_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_conferencesetting_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(add_default_values, remove_default_values)
    ]
