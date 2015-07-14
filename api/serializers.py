from rest_framework import serializers
from api.models import Entry


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('key', 'value', 'is_public', 'updated')
        # fields = ('value', 'is_public', 'created', 'updated')
