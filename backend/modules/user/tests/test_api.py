from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

User = get_user_model()


class GetMeViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            id='1',
            name='admin',
            email='admin@email.com',
            username='admin',
            password='password',
        )
        refresh = RefreshToken.for_user(self.user)
        self.url = 'http://127.0.0.1:8000/me'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_get_owner_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'admin')

    def test_admin_permission(self):
        self.user = User.objects.create_user(
            id='2',
            name='User',
            email='user@email.com',
            username='user',
            password='password',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OwnerViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            id='1',
            name='admin',
            email='admin@email.com',
            username='admin',
            password='password',
        )
        refresh = RefreshToken.for_user(self.user)    
        self.url = 'http://127.0.0.1:8000/owner'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_create_owner(self):
        data = {
            "id": "2",
            "name": "admin2",
            "email": "admin2@email.com",
            "username": "admin2",
            "password": "password"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'admin2')

    def test_create_owner_with_invalid_fields(self):
        data = {
            "id": "2",
            "name": "admin2",
            "email": "admin2@email.com",
            "user": "admin2",
            "password": "password"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_owner(self):
        data = { "username": "django"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'django')

    def test_update_owner_with_invalid_fields(self):
        data = { "user": "django"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_owner_check_password_field(self):
        data = { "password": "passed"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_owner(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

