# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0008_auto_20150601_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferenceproposalreviewer',
            name='nick',
            field=models.CharField(default='Reviewer', max_length=255, verbose_name='Nick Name'),
            preserve_default=True,
        ),
    ]
