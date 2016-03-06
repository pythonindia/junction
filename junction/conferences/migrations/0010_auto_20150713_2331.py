# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0009_conferenceproposalreviewer_nick'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceVenue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('latitude', models.DecimalField(max_digits=17, decimal_places=15)),
                ('longitudes', models.DecimalField(max_digits=19, decimal_places=16)),
                ('created_by', models.ForeignKey(related_name='created_conferencevenue_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_conferencevenue_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('name', models.CharField(max_length=100)),
                ('note', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(related_name='created_room_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_room_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('venue', models.ForeignKey(to='conferences.ConferenceVenue')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='conference',
            name='venue',
            field=models.ForeignKey(to='conferences.ConferenceVenue', null=True),
            preserve_default=True,
        ),
    ]
