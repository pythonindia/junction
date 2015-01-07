# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('name', models.CharField(max_length=255, verbose_name=b'Conference Name')),
                ('description', models.TextField(default=b'')),
                ('start_date', models.DateField(verbose_name=b'Start Date')),
                ('end_date', models.DateField(verbose_name=b'End Date')),
                ('status', models.CharField(max_length=255, verbose_name=b'Current Status', choices=[(0, b'Accepting Call for Proposals'), (1, b'Closed for Proposals'), (2, b'Accepting Votes')])),
                ('created_by', models.ForeignKey(related_name='created_conference_set', verbose_name=b'Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_conference_set', verbose_name=b'Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConferenceModerator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('active', models.BooleanField(default=True, verbose_name=b'Is Active?')),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_conferencemoderator_set', verbose_name=b'Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('moderator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='updated_conferencemoderator_set', verbose_name=b'Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConferenceProposalReviewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('active', models.BooleanField(default=True, verbose_name=b'Is Active?')),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_conferenceproposalreviewer_set', verbose_name=b'Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_conferenceproposalreviewer_set', verbose_name=b'Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('reviewer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='conferenceproposalreviewer',
            unique_together=set([('conference', 'reviewer')]),
        ),
    ]
