from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

User = get_user_model()


class MeViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            id='1',
            name='Name',
            email='name@email.com',
            username='name',
            password='password',
            is_staff='True',
            is_superuser='True',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_get_user_data(self):
        response = self.client.get('http://127.0.0.1:8000/me')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'name')

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

        response = self.client.get('http://127.0.0.1:8000/me')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
