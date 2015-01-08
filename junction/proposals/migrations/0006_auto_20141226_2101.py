# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0005_auto_20141223_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalcomment',
            name='visibility',
        ),
        migrations.AddField(
            model_name='proposalcomment',
            name='private',
            field=models.BooleanField(default=False, verbose_name=b'Is Private?'),
            preserve_default=True,
        ),
    ]
