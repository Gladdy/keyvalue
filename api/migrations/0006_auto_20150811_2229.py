# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150811_2221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apikey',
            old_name='key',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='key',
            new_name='entry_key',
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('entry_key', 'api_key')]),
        ),
    ]
