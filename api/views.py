from django.shortcuts import render

from rest_framework.decorators import api_view
from api.serializers import EntrySerializer

from api.utility import *


@api_view(['POST'])
def entry_list(request):

    # Allowed inputs
    # POST  /api/?api_key=KEY   value=SOMETHING [is_public={true false}]
    # POST  /api/               value=SOMETHING

    api_key = check_auth(request, None, allow_match=False, require_auth=False)

    if api_key is not False:
        entry = create_entry(request, request.data['value'], None, api_key)
        return c_resp(request,entry, status.HTTP_201_CREATED)
    else:
        return c_resp(request, None, status.HTTP_400_BAD_REQUEST, error='Invalid API key')


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def entry_detail(request, pk):

    # Allowed inputs
    # GET  /api/KEY                 entries with is_public == True
    # GET  /api/KEY?api_key=KEY     hidden entries: api_key needs to be the root key or matching with the creation key
    if request.method == 'GET':

        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return Response('Key not found', status=status.HTTP_400_BAD_REQUEST)

        if entry.is_public or check_auth(request, entry, contains_value=False):
            serializer = EntrySerializer(entry)
            return Response(serializer.data)
        else:
            return Response('Unauthorized GET, associated API key required!', status=status.HTTP_401_UNAUTHORIZED)

    # POST/PUT  /api/KEY?api_key=API_KEY value=SOMEVALUE [is_public={true false}]
    # Works for both keys already present and for new key-value pairs
    # Requires the value parameter to be set for the update
    # Requires a valid api_key (root or matching) when the entry already exists
    elif request.method == 'POST' or request.method == 'PUT':

        try:
            entry = Entry.objects.get(pk=pk)

            # Update existing object
            if check_auth(request, entry):
                entry.value = request.data
                entry.save()
            else:
                return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        except Entry.DoesNotExist:

            # Create a new object
            api_key = check_auth(request, None, allow_match=False)
            if api_key:
                try:
                    entry = Entry.objects.create(key=pk, value=request.data['value'], api_key=api_key)
                except Exception:
                    return Response('Could not create object', status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response('Supplied value_key without API key', status=status.HTTP_401_UNAUTHORIZED)

        serializer = EntrySerializer(entry)
        return Response(serializer.data)

    elif request.method == 'DELETE':

        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return Response('Key not found', status=status.HTTP_400_BAD_REQUEST)

        if check_auth(request, entry, allow_match=False, contains_value=False):
            entry.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Unauthorized DELETE, API root key required!', status=status.HTTP_401_UNAUTHORIZED)


def documentation(request):
    return render(request, 'api/documentation.html')