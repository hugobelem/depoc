import requests

from django.test import LiveServerTestCase

from modules.accounts.factories import UserFactory


class EmailOrUsernameBackendTest(LiveServerTestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_auth_with_email(self):
        url = f'{self.live_server_url}/token'
        data = {'username': self.user.email, 'password': 'password'}
        response = requests.request('POST', url, data=data)
        self.assertIs(response.status_code, 200)
