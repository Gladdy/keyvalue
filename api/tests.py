from django.test import TestCase, Client
from django.contrib.auth.models import User

from api.models import ApiKey, Entry
from keyvalue.views import setup_new_user
from django.core.urlresolvers import reverse

from keyvalue.settings import NO_API_USERNAME

import simplejson as json


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

    def test_post_anonymous(self):

        # Submit the value through an anonymous POST request
        r = self.client.post(reverse('api:root'), {"value": self.original_value})
        self.assertEqual(r.status_code, 201)

        data = json.loads(r.content)
        url = data['url']
        self.assertEqual(data['value'], self.original_value)

        # Try to fetch the value
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)

        self.assertEqual(data['value'], self.original_value)

    def test_post_api_key_no_public(self):
        r = self.login(self.username)

        # Fetch the non-root API key
        api_key = User.objects.get(username=self.username).apikey_set.get(is_key_root=None, is_key_generate=None)

        # Submit the value
        url = reverse('api:root')+'?api_key='+api_key.key
        r = self.client.post(url, {"value": self.original_value})
        self.assertEqual(r.status_code, 201)

        # Check whether the submission was correct
        data = json.loads(r.content)
        url = data['url']
        self.assertEqual(data['value'], self.original_value)

        # Fetch the value again (DENIED BECAUSE NO API KEY)
        r = self.client.get(url, {"value": self.original_value})
        self.assertEqual(r.status_code, 401)

        # Fetch the value again (Should work)
        r = self.client.get(url+'?api_key='+api_key.key)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data['value'], self.original_value)

    def test_post_api_key_false_public(self):
        r = self.login(self.username)

        # Fetch the non-root API key
        api_key = User.objects.get(username=self.username).apikey_set.get(is_key_root=None, is_key_generate=None)

        # Submit the value
        url = reverse('api:root')+'?api_key='+api_key.key
        r = self.client.post(url, {"value": self.original_value, "is_public": False})
        self.assertEqual(r.status_code, 201)

        # Check whether the submission was correct
        data = json.loads(r.content)
        url = data['url']
        self.assertEqual(data['value'], self.original_value)

        # Fetch the value again (DENIED BECAUSE NO API KEY)
        r = self.client.get(url, {"value": self.original_value})
        self.assertEqual(r.status_code, 401)

        # Fetch the value again (Should work)
        r = self.client.get(url+'?api_key='+api_key.key)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data['value'], self.original_value)

    def test_post_api_key_true_public(self):
        r = self.login(self.username)

        # Fetch the non-root API key
        api_key = User.objects.get(username=self.username).apikey_set.get(is_key_root=None, is_key_generate=None)

        # Submit the value
        url = reverse('api:root')+'?api_key='+api_key.key
        r = self.client.post(url, {"value": self.original_value, "is_public": True})
        self.assertEqual(r.status_code, 201)

        # Check whether the submission was correct
        data = json.loads(r.content)
        url = data['url']
        self.assertEqual(data['value'], self.original_value)

        # Fetch the value again (Should work)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data['value'], self.original_value)