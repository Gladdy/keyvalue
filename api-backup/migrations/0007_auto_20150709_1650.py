# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150709_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apikey',
            old_name='created',
            new_name='created_time',
        ),
        migrations.AddField(
            model_name='apikey',
            name='created_ip',
            field=models.CharField(null=True, default=None, max_length=45),
        ),
    ]
