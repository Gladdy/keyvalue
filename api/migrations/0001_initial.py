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
            name='Entry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=False)),
                ('key', models.CharField(unique=True, max_length=16, db_index=True)),
                ('value', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('created_ip', models.CharField(null=True, max_length=45, default=None)),
                ('is_key_root', models.NullBooleanField(default=None)),
                ('is_key_generate', models.NullBooleanField(default=None)),
                ('value', models.CharField(unique=True, max_length=16, db_index=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='token',
            field=models.ForeignKey(to='api.Token'),
        ),
        migrations.AlterUniqueTogether(
            name='token',
            unique_together=set([('user', 'is_key_generate'), ('user', 'is_key_root')]),
        ),
    ]
