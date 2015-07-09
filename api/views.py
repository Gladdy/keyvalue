from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Entry
from api.serializers import EntrySerializer

@api_view(['GET', 'POST'])
def entry_list(request):
    """
    List all code entries, or create a new entry.
    """
    if request.method == 'GET':
        entries = Entry.objects.all()
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def entry_detail(request, pk):
    """
    Retrieve, update or delete an entry.
    """
    try:
        entry = Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EntrySerializer(entry)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    entries = Entry.objects.all()
    return render(request, 'api/index.html', {'entries' : entries})
