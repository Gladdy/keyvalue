from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
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

    def get_root_version(self):
        if self.is_key_root:
            return self
        else:
            return self.user.token_set.get(is_key_root=True)

class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.ForeignKey(Token)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    key = models.CharField(max_length=16, db_index=True)
    value = models.TextField()

    # class Meta:
    #     unique_together = (('token', 'key'),)

    def __str__(self):
        return self.key

