# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("conferences", "0006_auto_20150216_1929"),
        ("proposals", "0003_auto_20150113_1401"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProposalSectionReviewer",
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
                    "conference_reviewer",
                    models.ForeignKey(
                        verbose_name="Conference Proposal Reviewers",
                        to="conferences.ConferenceProposalReviewer",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        related_name="created_proposalsectionreviewer_set",
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
                        related_name="updated_proposalsectionreviewer_set",
                        verbose_name="Modified By",
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "proposal_section",
                    models.ForeignKey(
                        verbose_name="Proposal Section",
                        to="proposals.ProposalSection",
                        on_delete=django.db.models.deletion.CASCADE,
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=(models.Model,),
        ),
    ]
