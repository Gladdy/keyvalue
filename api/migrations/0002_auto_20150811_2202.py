# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikey',
            name='testval',
        ),
        migrations.AlterField(
            model_name='entry',
            name='key',
            field=models.CharField(db_index=True, unique=True, max_length=16, null=True),
        ),
    ]
