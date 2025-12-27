import requests

from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

from .factories import UserFactory


class EmailOrUsernameBackendTest(LiveServerTestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_auth_with_email(self):
        url = f'{self.live_server_url}/token'
        data = {'username': self.user.email, 'password': 'password'}
        response = requests.request('POST', url, data=data)
        self.assertIs(response.status_code, 200)

class RegisterAccountTest(LiveServerTestCase):
    def test_hash_password(self):
        url = f'{self.live_server_url}/accounts'
        data = {
            'name': 'Test',
            'username': 'test',
            'email': 'test@email.com',
            'password': 'sdfgdsft345'
        }
        
        requests.request('POST', url, data=data)

        User = get_user_model()
        user = User.objects.get(username='test')

        self.assertTrue(user.check_password(data['password']))
        self.assertNotEqual(data['password'], user.password)