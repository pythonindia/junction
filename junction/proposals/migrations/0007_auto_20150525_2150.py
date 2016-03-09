# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_auto_20150416_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalSectionReviewerVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('role', models.PositiveSmallIntegerField(default=2, choices=[(1, 'Public'), (2, 'Reviewer')])),
                ('up_vote', models.BooleanField(default=True)),
                ('proposal', models.ForeignKey(to='proposals.Proposal')),
                ('voter', models.ForeignKey(to='proposals.ProposalSectionReviewer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='proposalsectionreviewervote',
            unique_together=set([('proposal', 'voter')]),
        ),
    ]
