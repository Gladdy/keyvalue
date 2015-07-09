from rest_framework import serializers
from api.models import Entry


class EntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields = ('key', 'user', 'value', 'created', 'updated')
