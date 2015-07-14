from django.test import TestCase, Client
from django.contrib.auth.models import User

from api.models import ApiKey, Entry
from keyvalue.views import setup_new_user
from django.core.urlresolvers import reverse

from keyvalue.settings import NO_API_USERNAME

import simplejson as json


def parse_json(json_bytes):

    print(json_bytes)
    json_str = json_bytes.decode('unicode_escape')
    print(json_str)

    if json_str[0] is '"':
        json_str = json_str[1:-1]

    return json.loads(json_str)


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

    def test_can_log_in_username(self):
        r = self.client.post(reverse('login'), {'id': self.username, 'password': self.password})
        r2 = self.client.get(reverse('logout'))
        self.assertEqual(r.status_code, 302)

    def test_can_log_in_email(self):
        r = self.client.post(reverse('login'), {'id': self.email, 'password': self.password})
        r2 = self.client.get(reverse('logout'))
        self.assertEqual(r.status_code, 302)

    def test_post_value(self):
        original_value = "UTF-8 thrown in: C λ aSH"

        # Submit the value through an anonymous POST request
        r = self.client.post(reverse('api:root'), {'value': original_value})
        self.assertEqual(r.status_code, 201)
        data = parse_json(r.content)
        url = data['url']

        # Try to fetch the value
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = parse_json(r.content)

        self.assertEqual(data['value'], original_value)


