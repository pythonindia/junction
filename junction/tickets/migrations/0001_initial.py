# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Third Party Stuff
import jsonfield.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('order_no', models.CharField(max_length=255)),
                ('order_cost', models.FloatField()),
                ('ticket_no', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=75)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('zipcode', models.IntegerField(null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('status', models.CharField(max_length=255)),
                ('others', jsonfield.fields.JSONField()),
                ('created_by', models.ForeignKey(related_name='created_ticket_set', verbose_name='Created By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('modified_by', models.ForeignKey(related_name='updated_ticket_set', verbose_name='Modified By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
