from rest_framework import status
from rest_framework.response import Response
from api.models import Entry, ApiKey
from django.contrib.auth.models import User
from keyvalue.utility import random_string
from distutils.util import strtobool
from django.core.urlresolvers import reverse
from api.serializers import EntrySerializer

def create_entry(value, api_key, **kwargs):
    """
    Repeatedly attempt to create an entry for the value using the given api_key.
    This function is guaranteed to succeed unless the primary keys have been exhausted (~5E28)
    :param value:
    :param api_key:
    :param kwargs:
    :return: a successful entry into the database
    """

    if 'key' in kwargs:
        key = kwargs['key']

        if len(key) > 16:
            raise ValueError("Key is too long (max length: 16)")

        return Entry.objects.create(value=value, api_key=api_key, **kwargs)

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
    """
    Create a response for the request.
    :param request:
    :param code: The status code of the response
    :param kwargs: Possibilities:
                    - response, for traffic from the app to the client
                    - error, reporting the errors
    :return: A djangorestframework Response object
    """

    if 'entry' in kwargs:
        if 'many' in kwargs:
            response = EntrySerializer(kwargs['entry'], many=kwargs['many'])
        else:
            response = EntrySerializer(kwargs['entry'])

        return Response(response.data, code, content_type='application/json')

    elements = {}

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


def check_api_key(request, entry, check_root=True, check_match=True):

    if 'api_key' in request.GET:
        try:
            api_key = ApiKey.objects.get(pk=request.GET['api_key'])
        except ApiKey.DoesNotExist:
            raise ValueError('Invalid API key')

        # If only creating an element, having a valid API key is sufficient
        if entry is None:
            return api_key

        # Check all
        access = False
        if check_match and entry is not None:
            if entry.api_key.key == api_key.key:
                access = True

        if check_root and entry is not None:
            if entry.api_key.user == api_key.user and api_key.is_key_root:
                access = True

        if access:
            return api_key
        else:
            raise ValueError('Unauthorized API key for this operation')

    else:
        raise ValueError('You should have supplied an API key')

def check_has_time(request, api_key, default=None):

    if 'timeout' in request.data:



        return request.data['value']
    elif default is not None:
        return default
    else:
        raise ValueError('Please supply a value in the request')


def check_has_value(request, api_key, default=None):
    if 'value' in request.data:
        return request.data['value']
    elif default is not None:
        return default
    else:
        raise ValueError('Please supply a value in the request')