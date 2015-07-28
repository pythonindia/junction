# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0010_auto_20150713_2331'),
        ('proposals', '0013_proposalcomment_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalProposal',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('created_at', models.DateTimeField(verbose_name='Created At', editable=False, blank=True)),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', editable=False, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=('title',), max_length=255, editable=False, blank=True)),
                ('description', models.TextField(default='')),
                ('target_audience', models.PositiveSmallIntegerField(default=1, verbose_name='Target Audience', choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced')])),
                ('prerequisites', models.TextField(default='', blank=True)),
                ('content_urls', models.TextField(default='', blank=True)),
                ('speaker_info', models.TextField(default='', blank=True)),
                ('speaker_links', models.TextField(default='', blank=True)),
                ('status', models.PositiveSmallIntegerField(default=1, choices=[(2, 'Public'), (1, 'Draft'), (3, 'Cancelled')])),
                ('review_status', models.PositiveSmallIntegerField(default=1, verbose_name='Review Status', choices=[(1, 'Yet to be reviewed'), (2, 'Selected'), (3, 'Rejected'), (4, 'On hold'), (5, 'Wait-listed')])),
                ('deleted', models.BooleanField(default=False, verbose_name='Is Deleted?')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('author', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('conference', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='conferences.Conference', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('proposal_section', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='proposals.ProposalSection', null=True)),
                ('proposal_type', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='proposals.ProposalType', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical proposal',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricalProposalSectionReviewerVote',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('created_at', models.DateTimeField(verbose_name='Created At', editable=False, blank=True)),
                ('modified_at', models.DateTimeField(verbose_name='Last Modified At', editable=False, blank=True)),
                ('role', models.PositiveSmallIntegerField(default=2, choices=[(1, 'Public'), (2, 'Reviewer')])),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('proposal', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='proposals.Proposal', null=True)),
                ('vote_value', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='proposals.ProposalSectionReviewerVoteValue', null=True)),
                ('voter', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='proposals.ProposalSectionReviewer', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical histPropSectionReviewerVote',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='proposalsectionreviewervote',
            options={'verbose_name': 'histPropSectionReviewerVote'},
        ),
        migrations.AlterField(
            model_name='proposalcomment',
            name='vote',
            field=models.BooleanField(default=False, verbose_name='What is the reason?'),
            preserve_default=True,
        ),
    ]
