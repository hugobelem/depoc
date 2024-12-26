from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from modules.business.models import Business, BusinessOwner

from . import factories

User = get_user_model()


class TestBusinessEndpointView(APITestCase):
    def setUp(self):
        self.owner = factories.OwnerFactory()
        self.business = factories.BusinessFactory(legalName='The Main Biz')
        self.business_owner = factories.BusinessOwnerFactory(
            owner=self.owner,
            business=self.business
        )

        refresh = RefreshToken.for_user(self.owner)
        self.url = 'http://127.0.0.1:8000/business'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_permission(self):
        '''
        The permission class for the BusinessEndpoint view is [IsAdminUser].
        Test if a member with no permision can access the endpoint.
        '''
        member = factories.MemberFactory()

        refresh = RefreshToken.for_user(member)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_post_business(self):
        '''
        Send a POST request to create a business.
        - Only owners can create a business.
        - An owner is a User model instance with
          the is_superuser attribute set to True.
        '''
        owner = factories.OwnerFactory()

        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        data = {
            'legalName': 'Business Inc',
            'tradeName': 'Biz',
            'registrationNumber': '01234567891234',
        }
        
        response = client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['details']['legalName'], 'Business Inc')


    def test_post_business_when_owner_has_one(self):
        '''
        Send a POST request to create a business when the Owner making 
        the request is already linked to an existing business.
        '''
        data = {
            'legalName': 'Business Inc',
            'tradeName': 'Biz',
            'registrationNumber': '01234567891235',
        }
        response = self.client.post(self.url, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_business_with_empty_data(self):
        '''
        Send a POST request with empy data to create a business.
        '''
        owner = factories.OwnerFactory()

        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        data = {}

        response = client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_business_with_invalid_fields(self):
        owner = factories.OwnerFactory()

        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        data = {
            'name': 'Business Inc',
            'tradeName': 'Biz',
            'registrationNumber': '01234567891236',
        }

        response = client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_business(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.data['details']['legalName'], 'The Main Biz')


    def test_get_business_when_owner_dont_have_one(self):
        owner = factories.OwnerFactory()
             
        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token) 

        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_inactive_business(self):
        self.business.active = False
        self.business.save()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        


    def test_patch_business(self):
        data = {'tradeName': 'Corporate Biz'}

        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

        updated_business = Business.objects.get(pk=self.business.id)
        self.assertEqual(updated_business.tradeName, data['tradeName'])
    

    def test_patch_business_when_owner_dont_have_one(self):
        owner = factories.OwnerFactory()

        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token) 

        response = client.patch(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        


    def test_patch_inactive_business(self):
        self.business.active = False
        self.business.save()

        data = {
            'tradeName': 'Corporate Biz'
        }

        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)        


    def test_patch_business_with_empty_data(self):
        data = {}
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)   


    def test_patch_business_with_invalid_fields(self):
        data = {'name': 'Corporate Biz'}
        response = self.client.patch(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       


    def test_delete_business(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         

    def test_delete_business_when_owner_dont_have_one(self):
        owner = factories.OwnerFactory()

        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token) 

        response = client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)    
         

    def test_delete_inactive_business(self):
        self.business.active = False
        self.business.save()
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)