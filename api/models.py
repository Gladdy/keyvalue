from django.db import models
from django.contrib.auth.models import User
from keyvalue.settings import NO_API_USERNAME


class ApiKey(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    created_ip = models.CharField(max_length=45, null=True, default=None)

    is_key_root = models.NullBooleanField(default=None)
    is_key_generate = models.NullBooleanField(default=None)

    value = models.CharField(max_length=16, unique=True, db_index=True)

    class Meta:
        unique_together = (('user', 'is_key_root'), ('user', 'is_key_generate'),)

    def __str__(self):
        return self.value


class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    entry_key = models.CharField(max_length=16, unique=True, db_index=True, null=True, blank=True)

    api_key = models.ForeignKey(ApiKey)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_public = models.BooleanField(default=False)

    value = models.TextField()


    class Meta:
        unique_together = (('entry_key', 'api_key'),)

    def __str__(self):
        return self.entry_key

