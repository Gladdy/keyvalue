from rest_framework.permissions import BasePermission
from rest_framework import exceptions

from api.models import Entry
from api.serializers import public_domain_token

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

def get_token_header(request):

    if 'token' in request.GET:
        return request.GET['token']
    elif 'token' in request.data:
        return request.data['token']
    elif 'HTTP_AUTHORIZATION' in request.META:
        return request.META['HTTP_AUTHORIZATION']
    else:
        return None


class IsAuthenticatedApiKey(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):

        try:
            entry = Entry.objects.get(key=view.kwargs['pk'])
        except Entry.DoesNotExist:
            raise exceptions.NotFound

        # Give read access on all public values (public domain and private values set to public) to everyone
        if entry.is_public and request.method in SAFE_METHODS:
            return True

        # Block write access to values in the public domain
        if entry.token.value == public_domain_token.value and request.method not in SAFE_METHODS:
            return False


        token = get_token_header(request)

        # A token is required for the other options
        if token is None:
            return False

        # Give read and write access on values that were made with the same api key
        if token == entry.token.value:
            return True

        # Give read and write access on values that were made with the users root key
        if token == entry.token.get_root_version().value:
            return True

        return False