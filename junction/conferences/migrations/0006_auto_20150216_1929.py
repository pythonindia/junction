# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0005_emailreviewernotificationsetting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailreviewernotificationsetting',
            name='conference_reviewer',
        ),
        migrations.RemoveField(
            model_name='emailreviewernotificationsetting',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='emailreviewernotificationsetting',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='emailreviewernotificationsetting',
            name='proposal_section',
        ),
        migrations.RemoveField(
            model_name='emailreviewernotificationsetting',
            name='proposal_type',
        ),
        migrations.DeleteModel(
            name='EmailReviewerNotificationSetting',
        ),
    ]
