# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_extensions.db.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("conferences", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConferenceProposalSection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "active",
                    models.BooleanField(default=True, verbose_name="Is Active?"),
                ),
                (
                    "conference",
                    models.ForeignKey(
                        to="conferences.Conference",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="created_conferenceproposalsection_set",
                        verbose_name="Created By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        related_name="updated_conferenceproposalsection_set",
                        verbose_name="Modified By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ConferenceProposalType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "active",
                    models.BooleanField(default=True, verbose_name="Is Active?"),
                ),
                (
                    "conference",
                    models.ForeignKey(
                        to="conferences.Conference",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="created_conferenceproposaltype_set",
                        verbose_name="Created By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        related_name="updated_conferenceproposaltype_set",
                        verbose_name="Modified By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Proposal",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        populate_from=("title",),
                        max_length=255,
                        editable=False,
                        blank=True,
                    ),
                ),
                ("description", models.TextField(default="")),
                (
                    "target_audience",
                    models.PositiveSmallIntegerField(
                        default=1,
                        verbose_name="Target Audience",
                        choices=[
                            (1, b"Beginner"),
                            (2, b"Intermediate"),
                            (3, b"Advanced"),
                        ],
                    ),
                ),
                ("prerequisites", models.TextField(default="")),
                ("content_urls", models.TextField(default="")),
                ("speaker_info", models.TextField(default="")),
                ("speaker_links", models.TextField(default="")),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        default=1,
                        choices=[(1, b"Draft"), (2, b"Public"), (3, b"Cancelled")],
                    ),
                ),
                (
                    "review_status",
                    models.PositiveSmallIntegerField(
                        default=1,
                        verbose_name="Review Status",
                        choices=[
                            (1, b"Yet to be reviewed"),
                            (2, b"Selected"),
                            (3, b"Rejected"),
                            (4, b" On hold"),
                            (5, b"Wait-listed"),
                        ],
                    ),
                ),
                (
                    "deleted",
                    models.BooleanField(default=False, verbose_name="Is Deleted?"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        verbose_name="Primary Speaker",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
                (
                    "conference",
                    models.ForeignKey(
                        to="conferences.Conference",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ProposalComment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "private",
                    models.BooleanField(default=False, verbose_name="Is Private?"),
                ),
                ("comment", models.TextField()),
                (
                    "deleted",
                    models.BooleanField(default=False, verbose_name="Is Deleted?"),
                ),
                (
                    "commenter",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
                (
                    "proposal",
                    models.ForeignKey(
                        to="proposals.Proposal",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ProposalCommentVote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                ("up_vote", models.BooleanField(default=True)),
                (
                    "proposal_comment",
                    models.ForeignKey(
                        to="proposals.ProposalComment",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ProposalSection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Proposal Section Name"
                    ),
                ),
                ("description", models.TextField(default="")),
                (
                    "active",
                    models.BooleanField(default=True, verbose_name="Is Active?"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="created_proposalsection_set",
                        verbose_name="Created By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        related_name="updated_proposalsection_set",
                        verbose_name="Modified By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ProposalType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Proposal Type Name"),
                ),
                ("description", models.TextField(default="")),
                (
                    "active",
                    models.BooleanField(default=True, verbose_name="Is Active?"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="created_proposaltype_set",
                        verbose_name="Created By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        related_name="updated_proposaltype_set",
                        verbose_name="Modified By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ProposalVote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "modified_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "role",
                    models.PositiveSmallIntegerField(
                        default=1, choices=[(1, b"Public"), (2, b"Reviewer")]
                    ),
                ),
                ("up_vote", models.BooleanField(default=True)),
                (
                    "proposal",
                    models.ForeignKey(
                        to="proposals.Proposal",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="proposalvote", unique_together=set([("proposal", "voter")]),
        ),
        migrations.AlterUniqueTogether(
            name="proposalcommentvote",
            unique_together=set([("proposal_comment", "voter")]),
        ),
        migrations.AddField(
            model_name="proposal",
            name="proposal_section",
            field=models.ForeignKey(
                verbose_name="Proposal Section",
                to="proposals.ProposalSection",
                on_delete=django.db.models.deletion.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="proposal",
            name="proposal_type",
            field=models.ForeignKey(
                verbose_name="Proposal Type",
                to="proposals.ProposalType",
                on_delete=django.db.models.deletion.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="proposal", unique_together=set([("conference", "slug")]),
        ),
        migrations.AddField(
            model_name="conferenceproposaltype",
            name="proposal_type",
            field=models.ForeignKey(
                verbose_name="Proposal Type",
                to="proposals.ProposalType",
                on_delete=django.db.models.deletion.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="conferenceproposaltype",
            unique_together=set([("conference", "proposal_type")]),
        ),
        migrations.AddField(
            model_name="conferenceproposalsection",
            name="proposal_section",
            field=models.ForeignKey(
                verbose_name="Proposal Section",
                to="proposals.ProposalSection",
                on_delete=django.db.models.deletion.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name="conferenceproposalsection",
            unique_together=set([("conference", "proposal_section")]),
        ),
    ]
