from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from modules.accounts.views import MeEndpoint, AccountsEndpoint, OwnerEndpoint
from modules.accounts.models import User

from .factories import UserFactory


class MeEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_authenticated(self):
        request = self.factory.get('me', HTTP_AUTHORIZATION=self.auth_header)
        response = MeEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 200)


class AccountsEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_allow_any_on_creation(self):
        data = {
            'name': 'User',
            'email': 'user@exemple.com',
            'username': 'user',
            'password': 'userspassword',
        }

        request = self.factory.post('accounts', data=data)
        response = AccountsEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_user_has_owner_attr(self):
        data = {
            'name': 'User',
            'email': 'user@exemple.com',
            'username': 'user',
            'password': 'userspassword',
        }
        request = self.factory.post('accounts', data=data)
        AccountsEndpoint.as_view()(request)
        user = User.objects.get(email='user@exemple.com')
        self.assertTrue(user.owner)

    def test_required_params_on_creation(self):
        data = {
            'name': 'User',
            'email': 'user@exemple.com',
            'password': 'userspassword',
        }
        request = self.factory.post('accounts', data=data)
        response = AccountsEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_user_is_staff_on_creation(self):
        data = {
            'name': 'User',
            'email': 'user@exemple.com',
            'password': 'userspassword',
        }
        request = self.factory.post('accounts', data=data)
        response = AccountsEndpoint.as_view()(request)
        json_respnse = response.data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_respnse['user']['is_staff'], True)

    def test_permission_is_authenticated_on_update(self):
        data = {
            'name': 'New User'
        }
        request = self.factory.patch('accounts', data=data)
        response = AccountsEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_update_password(self):
        data = {
            'password': 'password'
        }
        request = self.factory.patch(
            'accounts',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = AccountsEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_permission_is_owner_on_delete(self):
        request = self.factory.delete(
            'accounts',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = AccountsEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)


class OwnerEndpointViewtest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_owner(self):
        request = self.factory.get('owner', HTTP_AUTHORIZATION=self.auth_header)
        response = OwnerEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)
