# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150709_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apikey',
            old_name='is_generate',
            new_name='is_key_generate',
        ),
        migrations.RenameField(
            model_name='apikey',
            old_name='is_root',
            new_name='is_key_root',
        ),
        migrations.AlterUniqueTogether(
            name='apikey',
            unique_together=set([('user', 'is_key_generate'), ('user', 'is_key_root')]),
        ),
    ]
