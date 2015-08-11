# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150709_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='is_generate',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='is_root',
            field=models.NullBooleanField(default=None),
        ),
    ]
