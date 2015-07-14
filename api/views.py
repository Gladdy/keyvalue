from django.shortcuts import render

from rest_framework.decorators import api_view
from api.serializers import EntrySerializer

from api.utility import *
from keyvalue.settings import NO_API_USERNAME


@api_view(['POST'])
def entry_list(request):

    if 'api_key' in request.GET:
        # POST  /api/?api_key=KEY   value=SOMETHING [is_public={true default(false)}]
        try:
            is_public = check_is_public(request)
            api_key = check_api_key(request, None, override_valid=True)
            check_has_value(request)

            entry = create_entry(request.data['value'], api_key, is_public=is_public)
            return resp(request, status.HTTP_201_CREATED, entry=entry)

        except ValueError as e:
            return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))

    else:
        # POST  /api/               value=SOMETHING
        try:
            is_public = True
            api_key = User.objects.get(username=NO_API_USERNAME).apikey_set.get(is_key_generate=True)
            check_has_value(request)

            entry = create_entry(request.data['value'], api_key, is_public=is_public)
            return resp(request, status.HTTP_201_CREATED, entry=entry)

        except ValueError as e:
            return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
def entry_detail(request, pk):

    if request.method == 'GET':

        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return resp(request, status.HTTP_404_NOT_FOUND, error='Key does not exist')

        if entry.is_public:
            # GET  /api/KEY                 entries with is_public == True
            serializer = EntrySerializer(entry)
            return resp(request, status.HTTP_200_OK, response=serializer.data)
        else:
            # GET  /api/KEY?api_key=KEY     non public entries
            try:
                check_api_key(request, entry)
                serializer = EntrySerializer(entry)
                return resp(request, status.HTTP_200_OK, response=serializer.data)

            except ValueError as e:
                return resp(request, status.HTTP_401_UNAUTHORIZED, error=str(e))



    # POST/PUT  /api/KEY?api_key=API_KEY value=SOMEVALUE [is_public={true false}]
    # Works for both keys already present and for new key-value pairs
    # Requires the value parameter to be set for the update
    # Requires a valid api_key (root or matching) when the entry already exists
    elif request.method == 'POST' or request.method == 'PUT':

        try:
            entry = Entry.objects.get(pk=pk)

            try:
                check_api_key(request, entry)
                check_has_value(request)
                is_public = check_is_public(request, default=entry.is_public)

                entry.value = request.data['value']
                entry.is_public = is_public
                entry.save()

                serializer = EntrySerializer(entry)
                return resp(request, status.HTTP_200_OK, entry=entry, response=serializer.data)

            except ValueError as e:
                return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))

        except Entry.DoesNotExist:

            try:
                api_key = check_api_key(request, None, override_valid=True)
                check_has_value(request)
                is_public = check_is_public(request)

                entry = Entry.objects.create(key=pk, value=request.data['value'], api_key=api_key, is_public=is_public)

                serializer = EntrySerializer(entry)
                return resp(request, status.HTTP_200_OK, entry=entry, response=serializer.data)

            except ValueError as e:
                return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))
            except Exception as e:
                return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))

    elif request.method == 'DELETE':

        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return resp(request, status.HTTP_404_NOT_FOUND, error='Key does not exist')

        try:
            check_api_key(request, entry, check_match=False)
            entry.delete()
            return resp(request, status.HTTP_410_GONE)
        except ValueError as e:
            return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))


def documentation(request):
    return render(request, 'api/documentation.html')