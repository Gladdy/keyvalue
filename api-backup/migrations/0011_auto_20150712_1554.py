# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150712_1437'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='apikey',
            new_name='api_key',
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('key', 'api_key')]),
        ),
    ]
