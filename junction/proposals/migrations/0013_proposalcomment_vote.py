# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0012_auto_20150709_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalcomment',
            name='vote',
            field=models.BooleanField(default=False, verbose_name='Is Justification?'),
            preserve_default=True,
        ),
    ]
