# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_auto_20150913_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choicefeedbackquestion',
            name='is_required',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='textfeedbackquestion',
            name='is_required',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
