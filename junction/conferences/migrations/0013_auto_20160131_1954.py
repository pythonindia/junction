# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conferences', '0012_historicalconferenceproposalreviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='hashtags',
            field=models.CharField(max_length=100, default='', null=True, help_text="Used in social sharing, use commas to separate to tags, no '#' required.", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conference',
            name='twitter_id',
            field=models.CharField(max_length=100, default='', null=True, help_text='Used in social share widgets.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='conference',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, to='conferences.ConferenceVenue'),
            preserve_default=True,
        ),
    ]
