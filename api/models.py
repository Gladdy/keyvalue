from django.db import models
from django.contrib.auth.models import User

class ApiKey(models.Model):
    key = models.CharField(max_length=16, primary_key=True)
    user = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    created_ip = models.CharField(max_length=45, null=True, default=None)

    is_key_root = models.NullBooleanField(default=None)
    is_key_generate = models.NullBooleanField(default=None)

    class Meta:
        unique_together = (('user', 'is_key_root'), ('user', 'is_key_generate'),)

    def __str__(self):
        return self.key


class Entry(models.Model):
    key = models.CharField(max_length=16)
    value = models.TextField()
    user = models.ForeignKey(ApiKey, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('key', 'user'),)

    def __str__(self):
        return self.key

