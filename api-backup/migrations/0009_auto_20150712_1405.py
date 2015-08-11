# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_entry_is_public'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='user',
            new_name='apikey',
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('key', 'apikey')]),
        ),
    ]
