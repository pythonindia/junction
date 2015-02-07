# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0003_auto_20150113_1401'),
        ('conferences', '0004_conference_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotificationSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('conference', models.ForeignKey(related_name='email_notification', to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_emailnotificationsetting_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_emailnotificationsetting_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('proposal_section', models.ForeignKey(to='proposals.ProposalSection')),
                ('proposal_type', models.ForeignKey(to='proposals.ProposalType')),
            ],
            options={
                'verbose_name': 'email notification',
                'verbose_name_plural': 'email notifications',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='conferenceproposalreviewer',
            name='notifications',
            field=models.ManyToManyField(to='conferences.EmailNotificationSetting', null=True, blank=True),
            preserve_default=True,
        ),
    ]
