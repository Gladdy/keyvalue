from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import simplejson as json

from keyvalue.views import setup_new_user
from keyvalue.settings import PUBLIC_DOMAIN_USERNAME
from rest_framework.test import APIClient
from rest_framework import status

class ApiTestCase(TestCase):

    def setUp(self):
        self.user_admin = User.objects.create_superuser('admin', '1@prostendo.com', 'test')
        setup_new_user(self.user_admin)

        self.user_no_token = User.objects.create_user(PUBLIC_DOMAIN_USERNAME, '2@prostendo.com', 'test')
        setup_new_user(self.user_no_token)

        self.username = 'Gladdyu'
        self.email = '3@prostendo.com'
        self.password = 'test'

        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        setup_new_user(self.user)

        self.client = APIClient()

        self.original_value = "UTF-8 thrown in: C λ aSH"
        self.key = 'testkey'
        self.token = User.objects.get(username=self.username).token_set.get(is_key_root=None, is_key_generate=None)
        self.root_key = User.objects.get(username=self.username).token_set.get(is_key_root=True)
        self.generate_key = User.objects.get(username=self.username).token_set.get(is_key_generate=True)

    def login(self, ids):
        return self.client.post(reverse('login'), {'id': ids, 'password': self.password})

    def logout(self):
        return self.client.get(reverse('logout'))

    def construct_url(self, key, token):
        base = reverse('api:list')

        if key is not None:
            base += (key + '/')

        if token is not None:
            base += ('?token='+token.value)

        return base

    def perform_request(self, key=None,token=None,method='GET',extra=None,result=200, printUrl=False):
        url = self.construct_url(key,token)

        if printUrl:
            print(url)

        if method == 'GET':
            r = self.client.get(url, extra, format='json')
        elif method == 'POST':
            r = self.client.post(url, extra, format='json')
        elif method == 'DELETE':
            r = self.client.delete(url, extra, format='json')
        elif method == 'PUT':
            r = self.client.put(url, extra, format='json')

        self.assertEqual(r.status_code, result)

        if len(r.content) == 0:
            return None

        return json.loads(r.content)

    """
    LOGGING IN
    """
    def test_can_log_in_username(self):
        r = self.login(self.username)
        r2 = self.logout()

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r2.status_code, 302)

    def test_can_log_in_email(self):
        r = self.login(self.email)
        r2 = self.logout()

        self.assertEqual(r.status_code, 302)
        self.assertEqual(r2.status_code, 302)
    """
    ANONYMOUS POST
    """
    def test_post_anonymous(self):
        # Submit the value through an anonymous POST request
        data = self.perform_request(method='POST', extra={"value": self.original_value}, result=status.HTTP_201_CREATED)
        self.assertEqual(data['value'], self.original_value)

        # Try to fetch the value
        data = self.perform_request(key=data['key'], method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)

    """
    TEST THE IS_PUBLIC BEHAVIOUR
    """
    def test_post_token_no_public(self):
        # Submit the value through a POST request with a token
        data = self.perform_request(token=self.token, method='POST',extra={"value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)

        # Try to fetch the value
        # Fails because no token
        self.perform_request(key=data['key'], method='GET',result=403)

        # Fetch the correct value finally by use of the API key
        data = self.perform_request(key=data['key'], token=self.token, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)


    def test_post_public_false(self):
        # Submit the value through an anonymous POST request
        data = self.perform_request(token=self.token, method='POST',extra={"value": self.original_value, "is_public": False}, result=201)
        self.assertEqual(data['value'], self.original_value)

        # Try to fetch the value
        # Fails because no api key
        self.perform_request(key=data['key'], method='GET',result=403)

        # Fetch the correct value finally by use of the API key
        data = self.perform_request(key=data['key'], token=self.token, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)

    def test_post_public_true(self):
        # Submit the value through an anonymous POST request
        data = self.perform_request(token=self.token, method='POST',extra={"value": self.original_value, "is_public": True}, result=201)
        self.assertEqual(data['value'], self.original_value)

        # Fetch the correct value finally without api key
        data = self.perform_request(key=data['key'], method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)

    """
    TEST POSTS OF SPECIFIC KEYS
    """
    def test_post_specific_key(self):
        data = self.perform_request(token=self.token, method='POST',extra={'key':self.key, "value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=data['key'], token=self.token, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

        # No result without API key
        data = self.perform_request(key=data['key'], method='GET',result=403)

    def test_post_specific_key_public(self):
        data = self.perform_request(token=self.token, method='POST',extra={'key':self.key, "value": self.original_value, 'is_public': True}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=data['key'], token=self.token, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

        data = self.perform_request(key=data['key'], method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

    def test_post_specific_key_no_token(self):
        data = self.perform_request(method='POST',extra={'key':self.key, "value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=data['key'], method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

    """
    UPDATING VALUES
    """
    def test_put_update_with_token(self):
        data = self.perform_request(token=self.token, method='POST',extra={'key':self.key, "value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        original_data = self.perform_request(key=self.key, token=self.token, method='GET',result=200)
        self.assertEqual(original_data['value'], self.original_value)
        self.assertEqual(original_data['key'],self.key)

        updated_value = "HELLO UPDATE"
        #sleep(1)

        data = self.perform_request(key=self.key, token=self.token, method='PUT',extra={'value': updated_value}, result=200)
        self.assertEqual(data['value'], updated_value)

        updated_data = self.perform_request(key=self.key, token=self.token, method='GET',result=200)
        self.assertEqual(updated_data['value'], updated_value)
        self.assertEqual(updated_data['key'],self.key)

        self.assertEqual(original_data['created'], updated_data['created'])
        #self.assertNotEqual(original_data['updated'],updated_data['updated'])

    """
    DELETING VALUES
    """
    def test_post_delete(self):
        data = self.perform_request(method='POST', token=self.token, extra={'key':self.key, "value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=self.key, token=self.token, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

        data = self.perform_request(key=self.key, token=self.token, method='DELETE', result=204)
        data = self.perform_request(key=self.key, token=self.token, method='GET',result=404)

    def test_post_delete_root_access(self):
        data = self.perform_request(method='POST', token=self.token, extra={'key':self.key,"value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=self.key, token=self.root_key, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

        data = self.perform_request(key=self.key, token=self.root_key, method='DELETE', result=204)
        data = self.perform_request(key=self.key, token=self.root_key, method='GET',result=404)

    def test_post_delete_unauthorized(self):
        data = self.perform_request(method='POST', token=self.token, extra={'key':self.key,"value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=self.key, token=self.token, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

        data = self.perform_request(key=self.key, token=self.generate_key,  method='DELETE', result=403)

        data = self.perform_request(key=self.key, token=self.root_key,      method='GET',result=200)
        data = self.perform_request(key=self.key, token=self.generate_key,  method='GET',result=403)
        data = self.perform_request(key=self.key, token=self.token,         method='GET',result=200)

        data = self.perform_request(key=self.key, token=self.token,         method='DELETE', result=204)

        data = self.perform_request(key=self.key, token=self.root_key,      method='GET',result=404)
        data = self.perform_request(key=self.key, token=self.generate_key,  method='GET',result=404)
        data = self.perform_request(key=self.key, token=self.token,         method='GET',result=404)