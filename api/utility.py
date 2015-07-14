from rest_framework import status
from rest_framework.response import Response
from api.models import Entry,ApiKey
from django.contrib.auth.models import User
from keyvalue.utility import random_string
from distutils.util import strtobool

import simplejson as json

from keyvalue.settings import NO_API_USERNAME


def check_auth(request, entry, allow_root=True, allow_match=True, contains_value=True, require_auth=True):
    """
    :param request: Django Rest Framework Request wrapper
    :param entry: The object to fetch/modify - inactive for only entering values without an API key
    :param allow_root:
    :param allow_match:
    :param contains_value:
    :param require_auth:
    :return: False when the check fails - api_key when the check succeeds
    """

    if contains_value:
        if 'value' not in request.data:
            return False

    if not require_auth:
        no_key_user = User.objects.get(username=NO_API_USERNAME)
        return ApiKey.objects.get(user=no_key_user, is_key_generate=True)

    # Validity of the supplied API key
    if 'api_key' in request.GET:
        try:
            api_key = ApiKey.objects.get(pk=request.GET['api_key'])

            # Does the supplied key match the one used to create the object
            if allow_match:
                if entry.api_key.key == api_key.key:
                    return True

            # If you supply your own root key, allow all modifications to your own data
            if allow_root:
                if request.user.is_authenticated() and api_key.user == request.user and api_key.is_key_root:
                    return True

            return api_key

        except ApiKey.DoesNotExist:
            return False
    else:
        return False


def create_entry(request, value, key, api_key):
    """
    :param request:
    :param value:
    :param key:
    :param api_key:
    :return:
    """

    # Check whether the value should be public
    if 'is_public' in request.POST:
        try:
            is_public = strtobool(request.POST['is_public'])
        except ValueError:
            return Response("Invalid value for 'is_public'", status=status.HTTP_400_BAD_REQUEST)
    else:
        is_public = True

    # Finally, create the entry
    if key is not None:
        entry = Entry.objects.create(key=key, value=value, is_public=is_public, api_key=api_key)
    else:
        success = False
        while not success:
            try:
                entry = Entry.objects.create(key=random_string(16), value=value, is_public=is_public, api_key=api_key)
                success = True
            except Exception as e:
                print(e)
                pass

    return entry


def c_resp(request, entry, code, **kwargs):

    # 'key': entry.key,

    if entry is not None:
        entrydict = {'url': request.build_absolute_uri(entry.key) + '/', 'value':entry.value}
    else:
        entrydict = {}

    kwargs.update(entrydict)
    json_string = json.dumps(kwargs, separators=(', ', ': '))

    return Response(json_string, code, content_type='application/json')
