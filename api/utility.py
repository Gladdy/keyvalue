from rest_framework import status
from rest_framework.response import Response
from api.models import Entry, ApiKey
from django.contrib.auth.models import User
from keyvalue.utility import random_string
from distutils.util import strtobool
from django.core.urlresolvers import reverse


def create_entry(value, api_key, **kwargs):

    # Finally, create the entry
    success = False
    while not success:
        try:
            entry = Entry.objects.create(key=random_string(16), value=value, api_key=api_key, **kwargs)
            success = True
        except Exception as e:
            print(e)
            pass

    return entry


def resp(request, code, **kwargs):

    elements = {}

    if 'entry' in kwargs:
        entry = kwargs['entry']
        url = reverse('api:root') + entry.key + '/'
        entry_dict = {'key': entry.key, 'url': url, 'value': entry.value}
        elements.update(entry_dict)

    if 'response' in kwargs:
        elements.update(kwargs['response'])

    if 'error' in kwargs:
        elements.update({'error': kwargs['error']})

    return Response(elements, code, content_type='application/json')


def check_is_public(request, default=False):
    # Check whether the value should be public
    if 'is_public' in request.data:
        try:
            is_public = strtobool(request.POST['is_public'])
        except ValueError as e:
            raise ValueError('Invalid value for "is_public"')
    else:
        is_public = default

    return is_public


def check_api_key(request, entry, override_valid=False, check_root=True, check_match=True):

    if 'api_key' in request.GET:
        try:
            api_key = ApiKey.objects.get(pk=request.GET['api_key'])
        except ApiKey.DoesNotExist:
            raise ValueError('Invalid API key')

        # If only creating an element, having an API key is sufficient
        if override_valid:
            return api_key

        # Check all
        access = False
        if check_match and entry is not None:
            if entry.api_key.key == api_key.key:
                access = True

        if check_root and entry is not None:
            print(entry.api_key.user)
            print(api_key.user)
            if entry.api_key.user == api_key.user and api_key.is_key_root:
                access = True

        if access:
            return api_key
        else:
            raise ValueError('Unauthorized API key for this operation')

    else:
        raise ValueError('You should have supplied an API key')


def check_has_value(request):
    if 'value' in request.data:
        return
    else:
        raise ValueError('Please supply a value in the request')


def get_entry(request, pk):
    try:
        return Entry.objects.get(pk=pk)
    except Entry.DoesNotExist:
        return resp(request, status.HTTP_200_OK, error='Key does not exist')