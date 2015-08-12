from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import Entry, Token
from api.permission import IsAuthenticatedApiKey, get_token_header
from api.serializers import EntrySerializer, EntrySerializerNoKey, EntrySerializerUpdater
from api.serializers import public_domain_token


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'entries': reverse('entry-list', request=request, format=format),
        'tokens':reverse('token-list', request=request, format=format),
    })


class EntryList(APIView):
    """
    List all entries in the public domain or create a new entry
    If you do not supply an API key your value will end up in the public domain, meaning that the value is immutable and visible to everyone who has the link.

    """

    def get(self, request, format=None):
        entries = Entry.objects.filter(is_public=True)
        serializer = EntrySerializer(entries,many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        # When you do not supply an API key, you automatically end up in the public space,
        # meaning that the value is immutable and visible to everyone who has the link

        token = get_token_header(request)
        #public_domain_token = User.objects.get(username=PUBLIC_DOMAIN_USERNAME).token_set.get(is_key_generate=True)

        if (token is None) or (token == public_domain_token.value):
            serializer = EntrySerializerNoKey(data=request.data)
        else:
            #update the request with the token supplied, in whatever way
            data_new = request.data.copy()
            data_new['token'] = token
            serializer = EntrySerializer(data=data_new)


        if serializer.is_valid():
            entry = serializer.save()

            # Compute the new access location
            location = request.build_absolute_uri().split('?')[0] + entry.key+'/'


            # no token      public          no key
            # yes token     public          append key
            # yes token     private         append key

            # No token or a public entry
            if token is not None:
                location += '?token=' + entry.token.value

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers={'Location':location})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntryDetail(APIView):
    """
    Retrieve, update or delete a single entry.
    Write access requires a token, either the accounts root token or the token used to create the entry.
    Values in the public domain (created without an API key) cannot be changed after creation
    """
    permission_classes = (IsAuthenticatedApiKey,)

    @staticmethod
    def get_object(key, request):
        try:
            # Code needed for the separation of duplicate keys - hereby disallowed. Might change in the future.

            # token = get_token_header(request)
            # if token is None:
            #     token = User.objects.get(username=PUBLIC_DOMAIN_USERNAME).token_set.get(is_key_generate=True)
            # else:
            #     token = Token.objects.get(value=token)

            return Entry.objects.get(key=key)
        except (Entry.DoesNotExist, Token.DoesNotExist):
            #print(Entry.objects.all())
            #print(Token.objects.all())
            raise Http404

    def get(self, request, pk, format=None):
        entry = self.get_object(pk, request)
        serializer = EntrySerializer(entry)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        entry = self.get_object(pk, request)
        serializer = EntrySerializerUpdater(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        entry = self.get_object(pk, request)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)