from django.shortcuts import render

from rest_framework.decorators import api_view

from api.utility import *
from keyvalue.settings import NO_API_USERNAME


@api_view(['GET', 'POST'])
def entry_list(request):

    if request.method == 'GET':
        # GET  /api/?api_key=API_KEY
        try:
            api_key = check_api_key(request, None)

            entries = Entry.objects.filter(api_key=api_key)
            return resp(request, status.HTTP_200_OK, entry=entries, many=True)

        except ValueError as e:
            return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))

    else:

        # POST  /api/?api_key=API_KEY   value=VALUE is_public={true false}
        if 'api_key' in request.GET:
            try:
                api_key = check_api_key(request, None)
                value = check_has_value(request, api_key)
                is_public = check_is_public(request)

                entry = create_entry(request.data['value'], api_key, is_public=is_public)
                return resp(request, status.HTTP_201_CREATED, entry=entry)

            except ValueError as e:
                return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))

        # POST  /api/               value=VALUE
        # Anonymous submission
        else:
            try:
                api_key = User.objects.get(username=NO_API_USERNAME).apikey_set.get(is_key_generate=True)
                value = check_has_value(request, api_key)
                is_public = True

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

        # GET  /api/KEY                     entries with is_public == True
        if entry.is_public:
            return resp(request, status.HTTP_200_OK, entry=entry)

        # GET  /api/KEY?api_key=API_KEY     non public entries
        else:
            try:
                check_api_key(request, entry)
                return resp(request, status.HTTP_200_OK, entry=entry)

            except ValueError as e:
                return resp(request, status.HTTP_401_UNAUTHORIZED, error=str(e))

    # POST and PUT have the same behaviour. Useful when the client only supports POST.
    elif request.method == 'POST' or request.method == 'PUT':

        # POST  /api/KEY?api_key=API_KEY value=VALUE
        # PUT   /api/KEY?api_key=API_KEY value=VALUE
        try:
            entry = Entry.objects.get(pk=pk)

            # Update the existing entry
            try:
                api_key = check_api_key(request, entry)
                value = check_has_value(request, api_key, default=entry.value)
                is_public = check_is_public(request, default=entry.is_public)

                entry.value = value
                entry.is_public = is_public
                entry.save()

                return resp(request, status.HTTP_200_OK, entry=entry)

            except ValueError as e:
                return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))

        except Entry.DoesNotExist:

            # Create a new entry
            try:
                api_key = check_api_key(request, None)
                value = check_has_value(request, api_key)
                is_public = check_is_public(request)

                entry = Entry.objects.create(key=pk, value=value, api_key=api_key, is_public=is_public)
                return resp(request, status.HTTP_200_OK, entry=entry)

            except ValueError as e:
                return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))
            except Exception as e:
                return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))

    elif request.method == 'DELETE':

        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return resp(request, status.HTTP_404_NOT_FOUND, error='Key does not exist')

        # DELETE  /api/KEY?api_key=API_KEY
        try:
            check_api_key(request, entry)
            entry.delete()
            return resp(request, status.HTTP_410_GONE)
        except ValueError as e:
            return resp(request, status.HTTP_400_BAD_REQUEST, error=str(e))
