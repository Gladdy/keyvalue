# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150811_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='entry_key',
            field=models.CharField(db_index=True, max_length=16, unique=True, null=True),
        ),
    ]
