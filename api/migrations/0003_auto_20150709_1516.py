# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150708_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='is_generate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='apikey',
            name='is_root',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=16, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='entry',
            name='key',
            field=models.CharField(max_length=16),
        ),
    ]
