from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from modules.business.models import Business, BusinessOwner

User = get_user_model()


class BusinessEndpoint(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            id='1',
            name='owner',
            email='owner@email.com',
            username='owner',
            password='ownerpassword',
        )
        self.business = Business.objects.create(
            legalName='Business Inc',
            tradeName='Biz',
            registrationNumber='01234567891230',
            active=True,
        )
        self.business_owner = BusinessOwner.objects.create(
            owner=self.owner,
            business=self.business
        )
        refresh = RefreshToken.for_user(self.owner)
        self.url = 'http://127.0.0.1:8000/business'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_business_endpoint_permission(self):
        self.user = User.objects.create_user(
            id='2',
            name='User',
            email='user@email.com',
            username='user',
            password='adminpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_business(self):
        self.admin = User.objects.create_superuser(
            id='3',
            name='admin',
            email='admin@email.com',
            username='admin',
            password='adminpassword',
        )        
        refresh = RefreshToken.for_user(self.admin)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        data = {
            'legalName': 'Business2 Inc',
            'tradeName': 'Biz2',
            'registrationNumber': '01234567891234',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['legalName'], 'Business2 Inc')


    def test_create_business_when_owner_already_has_one(self):
        data = {
            'legalName': 'Business3 Inc',
            'tradeName': 'Biz3',
            'registrationNumber': '01234567891235',
        }
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_business_with_empty_data(self):
        self.admin = User.objects.create_superuser(
            id='4',
            name='adminnew',
            email='adminnew@email.com',
            username='adminnew',
            password='adminpassword',
        )        
        refresh = RefreshToken.for_user(self.admin)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_business_with_invalid_fields(self):
        self.admin = User.objects.create_superuser(
            id='5',
            name='newadmin',
            email='newadmin@email.com',
            username='newadmin',
            password='adminpassword',
        )        
        refresh = RefreshToken.for_user(self.admin)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        
        data = {
            'name': 'Business4 Inc',
            'tradeName': 'Biz4',
            'registrationNumber': '01234567891236',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_business(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['legalName'], 'Business Inc')


    def test_retrieve_business_when_owner_dont_have_one(self):
        self.admin = User.objects.create_superuser(
            id='6',
            name='admin6',
            email='admin6@email.com',
            username='admin6',
            password='adminpassword',
        )        
        refresh = RefreshToken.for_user(self.admin)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token) 

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_retrieve_inactive_business(self):
        self.business.active = False
        self.business.save()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        


    def test_update_business(self):
        data = {
            'tradeName': 'Corporate Biz'
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

        updated_business = Business.objects.get(pk=self.business.id)
        self.assertEqual(updated_business.tradeName, data['tradeName'])
    

    def test_update_business_when_owner_dont_have_one(self):
        self.admin = User.objects.create_superuser(
            id='7',
            name='admin7',
            email='admin7@email.com',
            username='admin7',
            password='adminpassword',
        )        
        refresh = RefreshToken.for_user(self.admin)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token) 

        response = self.client.patch(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        


    def test_update_inactive_business(self):
        self.business.active = False
        self.business.save()
        data = {
            'tradeName': 'Corporate Biz'
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        


    def test_update_business_with_empty_data(self):
        data = {}
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)   


    def test_update_business_with_invalid_fields(self):
        data = {
            'name': 'Corporate Biz'
        }
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       


    def test_delete_business(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         

    def test_delete_business_when_owner_dont_have_one(self):
        self.admin = User.objects.create_superuser(
            id='8',
            name='admin8',
            email='admin8@email.com',
            username='admin8',
            password='adminpassword',
        )        
        refresh = RefreshToken.for_user(self.admin)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token) 

        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)    
         

    def test_delete_inactive_business(self):
        self.business.active = False
        self.business.save()
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)