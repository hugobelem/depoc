from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from . import factories

User = get_user_model()


class MeEndpointTest(APITestCase):
    def setUp(self):
        self.owner = factories.OwnerFactory(username='owner')

        refresh = RefreshToken.for_user(self.owner)
        self.url = 'http://127.0.0.1:8000/me'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_get_owner_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['details']['username'], 'owner')


    def test_permission(self):
        user = factories.UserFactory()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OwnerEndpointTest(APITestCase):
    def setUp(self):
        self.owner = factories.OwnerFactory(username='owner')

        refresh = RefreshToken.for_user(self.owner)
        self.url = 'http://127.0.0.1:8000/owner'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_post_owner(self):
        data = {
            "name": "admin",
            "email": "admin@email.com",
            "username": "admin",
            "password": "adminpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['details']['username'], 'admin')


    def test_post_owner_with_invalid_fields(self):
        data = {
            "name": "adminew",
            "email": "adminew@email.com",
            "user": "adminew",
            "password": "adminpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_owner_with_missing_fields(self):
        data = {
            "email": "adminewton@email.com",
            "username": "adminnewton",
            "password": "adminpassword"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)        


    def test_patch_owner(self):
        data = { "username": "django"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['details']['username'], 'django')


    def test_patch_owner_with_invalid_fields(self):
        data = { "user": "django"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_owner_password_field(self):
        data = { "password": "password"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_owner(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

