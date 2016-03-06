# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0007_auto_20150522_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='Current Status', choices=[(1, 'Accepting Proposals'), (2, 'Proposal submission closed'), (3, 'Accepting Votes'), (4, 'Schedule Published')]),
            preserve_default=True,
        ),
    ]
