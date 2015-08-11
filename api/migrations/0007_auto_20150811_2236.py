# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150811_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='entry_key',
            field=models.CharField(max_length=16, db_index=True, unique=True, blank=True),
        ),
    ]
