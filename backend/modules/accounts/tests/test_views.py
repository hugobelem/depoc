import requests

from django.test import LiveServerTestCase

from modules.accounts.factories import UserFactory


# class GetUserToken(LiveServerTestCase):
#     def setUp(self):
#         self.user = UserFactory()
#         url = f'{self.live_server_url}/token'
#         data = {'username': self.user.email, 'password': 'password'}
#         response = requests.request('POST', url, data=data)
#         tokens = response.json()
#         self.access_token = tokens.get('access')

#     def token(self):
#         return self.access_token


# class MeEndpointViewTest(LiveServerTestCase):
#     def setUp(self):
#         get_token = GetUserToken()
#         token = get_token.token()
#         print(token)

#     def test_permission_is_authenticated(self):
#         url = f'{self.live_server_url}/me'
#         headers = {'Authorization': f'Bearer {self.access_token}'}
#         response = requests.request('GET', url, headers=headers)
#         self.assertEqual(response.status_code, 200)

#         response = requests.request('GET', url)
#         self.assertEqual(response.status_code, 401)


class AccountsEndpointViewTest(LiveServerTestCase):
    def setUp(self):
        self.user = UserFactory()
        url = f'{self.live_server_url}/token'
        data = {'username': self.user.email, 'password': 'password'}
        response = requests.request('POST', url, data=data)
        tokens = response.json()
        self.access_token = tokens.get('access')


    def test_permission_allow_on_creation(self):
        data = {}
        
