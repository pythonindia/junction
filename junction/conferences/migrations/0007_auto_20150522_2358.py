# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0006_auto_20150216_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conference',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='Current Status', choices=[(1, 'Accepting Call for Proposals'), (2, 'Closed for Proposals'), (3, 'Accepting Votes'), (4, 'Schedule Published')]),
            preserve_default=True,
        ),
    ]
