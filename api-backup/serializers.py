from rest_framework import serializers
from api.models import Entry


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('value', 'is_public', 'created')
        # fields = ('value', 'is_public', 'created', 'updated')
