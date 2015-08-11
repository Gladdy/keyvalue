# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(db_index=True, unique=True, max_length=16)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('created_ip', models.CharField(default=None, null=True, max_length=45)),
                ('is_key_root', models.NullBooleanField(default=None)),
                ('is_key_generate', models.NullBooleanField(default=None)),
                ('testval', models.CharField(max_length=10)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(db_index=True, unique=True, max_length=16)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=False)),
                ('value', models.TextField()),
                ('api_key', models.ForeignKey(to='api.ApiKey')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('key', 'api_key')]),
        ),
        migrations.AlterUniqueTogether(
            name='apikey',
            unique_together=set([('user', 'is_key_root'), ('user', 'is_key_generate')]),
        ),
    ]
