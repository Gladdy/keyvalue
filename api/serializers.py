from django.forms import widgets
from rest_framework import serializers
from api.models import Entry


class EntrySerializer(serializers.Serializer):
    key = serializers.CharField(read_only=True, min_length=10, max_length=10)
    value = serializers.CharField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    def create(self, validated_data):
        return Entry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.key = validated_data.get('key', instance.key)
        instance.value = validated_data.get('value', instance.value)
        instance.created = validated_data.get('created', instance.created)
        instance.updated = validated_data.get('updated', instance.updated)
        instance.save()

        return instance
