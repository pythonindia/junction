# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0008_auto_20150528_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalSectionReviewerVoteValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('vote_value', models.SmallIntegerField()),
                ('description', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(related_name='created_proposalsectionreviewervotevalue_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_proposalsectionreviewervotevalue_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='proposalsectionreviewervote',
            name='vote_value',
            field=models.ForeignKey(to='proposals.ProposalSectionReviewerVoteValue'),
            preserve_default=True,
        ),
    ]
