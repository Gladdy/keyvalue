from django.test import TestCase, Client
from django.contrib.auth.models import User

from api.models import ApiKey, Entry
from keyvalue.views import setup_new_user
from django.core.urlresolvers import reverse

from keyvalue.settings import NO_API_USERNAME

import simplejson as json
from time import sleep

class ApiTestCase(TestCase):

    def setUp(self):
        self.user_admin = User.objects.create_superuser('admin', '1@prostendo.com', 'test')
        setup_new_user(self.user_admin)

        self.user_no_api_key = User.objects.create_superuser(NO_API_USERNAME, '2@prostendo.com', 'test')
        setup_new_user(self.user_no_api_key)

        self.user = User.objects.create_superuser('Gladdyu', '3@prostendo.com', 'test')
        setup_new_user(self.user)

        self.client = Client()
        self.username = 'Gladdyu'
        self.email = '3@prostendo.com'
        self.password = 'test'

        self.original_value = "UTF-8 thrown in: C λ aSH"
        self.key = 'testkey'
        self.api_key = User.objects.get(username=self.username).apikey_set.get(is_key_root=None, is_key_generate=None)

    def login(self, ids):
        return self.client.post(reverse('login'), {'id': ids, 'password': self.password})

    def logout(self):
        return self.client.get(reverse('logout'))

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

    def construct_url(self, key, api_key):
        base = reverse('api:root')

        if key is not None:
            base += (key + '/')

        if api_key is not None:
            base += ('?api_key='+api_key.key)

        return base

    def perform_request(self, key=None,api_key=None,method='GET',extra=None,result=200):
        url = self.construct_url(key,api_key)

        if method == 'GET':
            r = self.client.get(url, extra)
        elif method == 'POST':
            r = self.client.post(url, extra)
        elif method == 'DELETE':
            r = self.client.delete(url, extra)
        elif method == 'PUT':
            r = self.client.put(url, extra, content_type='application/json')

        self.assertEqual(r.status_code, result)

        return json.loads(r.content)

    """
    ANONYMOUS POST
    """
    def test_post_anonymous(self):
        # Submit the value through an anonymous POST request
        data = self.perform_request(method='POST',extra={"value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)

        # Try to fetch the value
        data = self.perform_request(key=data['key'],method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)

    """
    TEST THE IS_PUBLIC BEHAVIOUR
    """
    def test_post_api_key_no_public(self):
        # Submit the value through an anonymous POST request
        data = self.perform_request(api_key=self.api_key, method='POST',extra={"value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)

        # Try to fetch the value
        # Fails because no api key
        self.perform_request(key=data['key'], method='GET',result=401)

        # Fetch the correct value finally by use of the API key
        data = self.perform_request(key=data['key'], api_key=self.api_key, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)

    def test_post_public_false(self):
        # Submit the value through an anonymous POST request
        data = self.perform_request(api_key=self.api_key, method='POST',extra={"value": self.original_value, "is_public": False}, result=201)
        self.assertEqual(data['value'], self.original_value)

        # Try to fetch the value
        # Fails because no api key
        self.perform_request(key=data['key'], method='GET',result=401)

        # Fetch the correct value finally by use of the API key
        data = self.perform_request(key=data['key'], api_key=self.api_key, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)

    def test_post_public_true(self):
        # Submit the value through an anonymous POST request
        data = self.perform_request(api_key=self.api_key, method='POST',extra={"value": self.original_value, "is_public": True}, result=201)
        self.assertEqual(data['value'], self.original_value)

        # Fetch the correct value finally without api key
        data = self.perform_request(key=data['key'], method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)

    """
    TEST POSTS OF SPECIFIC KEYS
    """
    def test_post_specific_key(self):
        data = self.perform_request(key=self.key, api_key=self.api_key, method='POST',extra={"value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=data['key'], api_key=self.api_key, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

        # No result without API key
        data = self.perform_request(key=data['key'], method='GET',result=401)

    def test_post_specific_key_public(self):
        data = self.perform_request(key=self.key, api_key=self.api_key, method='POST',extra={"value": self.original_value, 'is_public': True}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        data = self.perform_request(key=data['key'], api_key=self.api_key, method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

        data = self.perform_request(key=data['key'], method='GET',result=200)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'],self.key)

    def test_post_specific_key_no_api_key(self):
        data = self.perform_request(key=self.key, method='POST',extra={"value": self.original_value}, result=400)

    """
    UPDATING VALUES
    """
    def test_post_update_with_api_key(self):
        data = self.perform_request(key=self.key, api_key=self.api_key, method='POST',extra={"value": self.original_value}, result=201)
        self.assertEqual(data['value'], self.original_value)
        self.assertEqual(data['key'], self.key)

        original_data = self.perform_request(key=self.key, api_key=self.api_key, method='GET',result=200)
        self.assertEqual(original_data['value'], self.original_value)
        self.assertEqual(original_data['key'],self.key)

        updated_value = "HELLO UPDATE"
        sleep(1)

        data = self.perform_request(key=self.key, api_key=self.api_key, method='POST',extra={"value": updated_value}, result=202)
        self.assertEqual(data['value'], updated_value)

        updated_data = self.perform_request(key=self.key, api_key=self.api_key, method='GET',result=200)
        self.assertEqual(updated_data['value'], updated_value)
        self.assertEqual(updated_data['key'],self.key)

        self.assertEqual(original_data['created'], updated_data['created'])
        self.assertNotEqual(original_data['updated'],updated_data['updated'])
