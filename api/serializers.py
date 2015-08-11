from rest_framework import serializers
from api.models import Entry
from django.contrib.auth.models import User
from keyvalue.settings import NO_API_USERNAME

no_api_user = User.objects.get(username=NO_API_USERNAME).apikey_set.get(is_key_generate=True)

class EntrySerializer(serializers.ModelSerializer):

    entry_key = serializers.CharField(read_only=True, required=False)

    api_key = serializers.CharField(max_length=16, default=no_api_user)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    is_public = serializers.BooleanField(required=False)

    class Meta:
        model = Entry
        fields = ('entry_key', 'api_key', 'created', 'updated','is_public', 'value' )