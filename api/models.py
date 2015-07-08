from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    key = models.CharField(max_length=10,primary_key=True)
    value = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
