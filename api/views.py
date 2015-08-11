from django.shortcuts import render

from rest_framework.decorators import api_view

from api.utility import *
from keyvalue.settings import NO_API_USERNAME

from api.models import Entry
from api.serializers import EntrySerializer
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class EntryList(APIView):
    """
    List all entries or create a new entry
    """

    def get(self, request, format=None):
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        data = request.data.copy()
        data['entry_key'] = random_string(8)
        data['is_public'] = True

        serializer = EntrySerializer(data=data)

        if serializer.is_valid():
            entry = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers={'Location':request.build_absolute_uri() + data['entry_key']+'/'})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class EntryDetail(APIView):
    """
    Retrieve a single entry, update or delete it
    """

    def get_object(self, key):
        try:
            return Entry.objects.get(entry_key=key)
        except Entry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        entry = self.get_object(pk)
        serializer = EntrySerializer(entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        entry = self.get_object(pk)
        serializer = EntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        entry = self.get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)