# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConferenceProposalSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('active', models.BooleanField(default=True, verbose_name=b'Is Active?')),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_conferenceproposalsection_set', verbose_name=b'Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_conferenceproposalsection_set', verbose_name=b'Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConferenceProposalType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('active', models.BooleanField(default=True, verbose_name=b'Is Active?')),
                ('conference', models.ForeignKey(to='conferences.Conference')),
                ('created_by', models.ForeignKey(related_name='created_conferenceproposaltype_set', verbose_name=b'Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_conferenceproposaltype_set', verbose_name=b'Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(default=b'')),
                ('target_audienance', models.TextField(default=b'')),
                ('prerequisites', models.TextField(default=b'')),
                ('content_urls', models.TextField(default=b'')),
                ('speaker_info', models.TextField(default=b'')),
                ('speaker_links', models.TextField(default=b'')),
                ('status', models.CharField(default=b'Draft', max_length=255, choices=[(0, b'Draft'), (1, b'Public'), (2, b'Cancelled')])),
                ('review_status', models.CharField(default=b'Yet to be reviewed', max_length=255, verbose_name=b'Review Status', choices=[(0, b'Yet to be reviewed'), (1, b'Selected'), (2, b'Rejected'), (3, b' On hold'), (4, b'Wait-listed')])),
                ('author', models.ForeignKey(verbose_name=b'Primary Speaker', to=settings.AUTH_USER_MODEL)),
                ('conference', models.ForeignKey(to='conferences.Conference')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('visibility', models.CharField(default=b'Public', max_length=255, choices=[(0, b'Public'), (1, b'Private')])),
                ('comment', models.TextField()),
                ('commenter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ForeignKey(to='proposals.Proposal')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalCommentVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('up_vote', models.BooleanField(default=True)),
                ('proposal_comment', models.ForeignKey(to='proposals.ProposalComment')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('name', models.CharField(max_length=255, verbose_name=b'Proposal Section Name')),
                ('description', models.TextField(default=b'')),
                ('active', models.BooleanField(default=True, verbose_name=b'Is Active?')),
                ('created_by', models.ForeignKey(related_name='created_proposalsection_set', verbose_name=b'Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_proposalsection_set', verbose_name=b'Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('name', models.CharField(max_length=255, verbose_name=b'Proposal Type Name')),
                ('description', models.TextField(default=b'')),
                ('active', models.BooleanField(default=True, verbose_name=b'Is Active?')),
                ('created_by', models.ForeignKey(related_name='created_proposaltype_set', verbose_name=b'Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_proposaltype_set', verbose_name=b'Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProposalVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'Last Modified At')),
                ('role', models.CharField(default=b'Public', max_length=255, choices=[(0, b'Public'), (1, b'Reviewer')])),
                ('up_vote', models.BooleanField(default=True)),
                ('proposal', models.ForeignKey(to='proposals.Proposal')),
                ('voter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='proposalvote',
            unique_together=set([('proposal', 'voter')]),
        ),
        migrations.AlterUniqueTogether(
            name='proposalcommentvote',
            unique_together=set([('proposal_comment', 'voter')]),
        ),
        migrations.AddField(
            model_name='proposal',
            name='proposal_section',
            field=models.ForeignKey(verbose_name=b'Proposal Section', to='proposals.ProposalSection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proposal',
            name='proposal_type',
            field=models.ForeignKey(verbose_name=b'Proposal Type', to='proposals.ProposalType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conferenceproposaltype',
            name='proposal_type',
            field=models.ForeignKey(verbose_name=b'Proposal Type', to='proposals.ProposalType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='conferenceproposaltype',
            unique_together=set([('conference', 'proposal_type')]),
        ),
        migrations.AddField(
            model_name='conferenceproposalsection',
            name='proposal_section',
            field=models.ForeignKey(verbose_name=b'Proposal Section', to='proposals.ProposalSection'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='conferenceproposalsection',
            unique_together=set([('conference', 'proposal_section')]),
        ),
    ]
