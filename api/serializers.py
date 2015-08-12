from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import Entry, Token
from keyvalue.settings import PUBLIC_DOMAIN_USERNAME
from keyvalue.utility import random_string

public_domain_token = User.objects.get(username=PUBLIC_DOMAIN_USERNAME).token_set.get(is_key_generate=True)

class EntrySerializerBase(serializers.ModelSerializer):
    key = serializers.CharField(required=False, default=lambda: random_string(8), max_length=16)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    value = serializers.CharField(required=True)

    class Meta:
        model = Entry
        fields = ('key', 'token', 'created', 'updated','is_public', 'value' )

class EntrySerializerNoKey(EntrySerializerBase):
    token = serializers.SlugRelatedField(queryset=Token.objects.all(), slug_field='value', required=False, default=lambda: User.objects.get(username=PUBLIC_DOMAIN_USERNAME).token_set.get(is_key_generate=True))
    is_public = serializers.BooleanField(required=False, default=True)


class EntrySerializer(EntrySerializerBase):
    token = serializers.SlugRelatedField(queryset=Token.objects.all(), slug_field='value')
    is_public = serializers.BooleanField(required=False, default=False)

class EntrySerializerUpdater(EntrySerializerBase):
    token = serializers.SlugRelatedField(slug_field='value', read_only=True)
    is_public = serializers.BooleanField(required=False)
    key = serializers.CharField(read_only=True)
    value = serializers.CharField(required=False)