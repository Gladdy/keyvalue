# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20150709_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
