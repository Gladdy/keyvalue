from django.db import models
from django.contrib.auth.models import User

class ApiKey(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class Entry(models.Model):
    key = models.CharField(max_length=32)
    value = models.TextField()
    user = models.ForeignKey(ApiKey, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('key', 'user'),)

    def __str__(self):
        return self.key

