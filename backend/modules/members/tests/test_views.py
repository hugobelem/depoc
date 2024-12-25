from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.apps import apps

from modules.members.models import Members

User = get_user_model()
Business = apps.get_model('modules_business', 'Business')
BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')

class MembersEndpointTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            id='J23O4K2J3R93URP2OI3J2323KK',
            name='Owner',
            username='owner',
            email='owner@email.com',
            password='theownerpassword',
        )
        self.business = Business.objects.create(
            legalName='Business Inc',
            tradeName='Biz',
            registrationNumber='01234567891230',
        )
        self.business_owner = BusinessOwner.objects.create(
            owner=self.owner,
            business=self.business
        )        
        refresh = RefreshToken.for_user(self.owner)
        self.url = 'http://127.0.0.1:8000/members'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_members_endpoint_permission(self):
        user = User.objects.create_user(
            id='1',
            name='User',
            email='user@email.com',
            username='user',
            password='adminpassword',
        )
        refresh = RefreshToken.for_user(user)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_member_creation(self):
        data = {
            'firstName': 'The',
            'lastName': 'Member',
            'taxId': '12345678901',
            'email': 'member@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_member_creation_whithout_registered_business(self):
        second_owner = User.objects.create_superuser(
            id='J23O4K2J3R93URP2OI3J23239K',
            name='Second Owner',
            username='secondowner',
            email='secondowner@email.com',
            password='thesecondownerpassword',
        )
        refresh = RefreshToken.for_user(second_owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {
            'firstName': 'The Second',
            'lastName': 'Member',
            'taxId': '12345678902',
            'email': 'secondmember@email.com',
            'access': 'True',
        }
        response = client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_member_creation_with_deactivated_business(self):
        self.business.active = False
        self.business.save()

        data = {
            'firstName': 'The Third',
            'lastName': 'Member',
            'taxId': '12345678903',
            'email': 'thirdmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_member_creation_with_no_data(self):
        data = {}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_member_creation_with_invalid_fields(self):
        data = {
            'first_name': 'The Fourth',
            'lastName': 'Member',
            'taxId': '12345678904',
            'email': 'fourthmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_member_creation_with_failed_validation(self):
        Members.objects.create(
            firstName='The Fifth',
            lastName='Member',
            email='fifthmember@email.com',
            access='True',
        )
        data = {
            'firstName': 'The Fifth',
            'lastName': 'Member',
            'taxId': '12345678905',
            'email': 'fifthmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrieve_members(self):
        data = {
            'firstName': 'The Sixth',
            'lastName': 'Member',
            'taxId': '12345678906',
            'email': 'sixthmember@email.com',
            'access': 'True',
        }
        self.client.post(self.url, data=data, format='json')
        data = {
            'firstName': 'The Seventh',
            'lastName': 'Member',
            'taxId': '12345678907',
            'email': 'seventhmember@email.com',
            'access': 'True',
        }
        self.client.post(self.url, data=data, format='json')
        
        response = self.client.get(self.url, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]['details']['firstName'], 'The Sixth')
        self.assertEqual(response_json[1]['details']['firstName'], 'The Seventh')


    def test_retrieve_member_whithout_registered_business(self):
        third_owner = User.objects.create_superuser(
            id='J23O4K2J3R93URP2OI3J23239K',
            name='Third Owner',
            username='thirdowner',
            email='thirdowner@email.com',
            password='thethirdownerpassword',
        )
        refresh = RefreshToken.for_user(third_owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_member_with_deactivated_business(self):
        data = {
            'firstName': 'The Eighth',
            'lastName': 'Member',
            'taxId': '12345678903',
            'email': 'eighthmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response_json['details']['firstName'], 'The Eighth')

        self.business.active = False
        self.business.save()

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_retrieve_one_member(self):
        data = {
            'firstName': 'The Nineth',
            'lastName': 'Member',
            'taxId': '12345678907',
            'email': 'ninethmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        member_id = response_json['id']
        
        url = f'http://127.0.0.1:8000/members/{member_id}'
        response = self.client.get(url, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['details']['firstName'], 'The Nineth')


    def test_retrieve_business_with_no_registered_members(self):
        url = f'http://127.0.0.1:8000/members/23432'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_retrieve_not_existing_member(self):
        data = {
            'firstName': 'The Nineth',
            'lastName': 'Member',
            'taxId': '19345678908',
            'email': 'ninethmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        
        url = f'http://127.0.0.1:8000/members/0'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_update_member(self):
        data = {
            'firstName': 'The 14',
            'lastName': 'Member',
            'taxId': '12345678309',
            'email': '14member@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        member_id = response_json['id']

        data = {
            'firstName': 'The Tenth',
        }
        
        url = f'http://127.0.0.1:8000/members/{member_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['details']['firstName'], 'The Tenth')


    def test_update_member_whithout_registered_business(self):
        fourth_owner = User.objects.create_superuser(
            id='J23O4K2J3R93URP2OI3J23239K',
            name='fourth Owner',
            username='fourthowner',
            email='fourthowner@email.com',
            password='thefourthownerpassword',
        )
        refresh = RefreshToken.for_user(fourth_owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        data = {
            'firstName': 'The Unkown',
        }
        
        url = f'http://127.0.0.1:8000/members/12'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_update_member_with_deactivated_business(self):
        data = {
            'firstName': 'The 2',
            'lastName': 'Member',
            'taxId': '12345678903',
            'email': 'eleventhmember@email.com',
            'access': 'True',
        }
        self.client.post(self.url, data=data, format='json')

        self.business.active = False
        self.business.save()

        data = {
            'firstName': 'The Eleventh',
        }

        url = f'http://127.0.0.1:8000/members/98'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_business_with_no_registered_members(self):
        data = {
            'firstName': 'The 72',
        }
        url = f'http://127.0.0.1:8000/members/72'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_member_with_no_data(self):
        data = {
            'firstName': 'The 12',
            'lastName': 'Member',
            'taxId': '12345678909',
            'email': '12member@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        member_id = response_json['id']

        data = {}
        
        url = f'http://127.0.0.1:8000/members/{member_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_not_existing_member(self):
        data = {
            'firstName': 'The 13',
            'lastName': 'Member',
            'taxId': '12345678908',
            'email': '13member@email.com',
            'access': 'True',
        }
        self.client.post(self.url, data=data, format='json')
        
        data = {'firstName': 'The 1203',}
        
        url = f'http://127.0.0.1:8000/members/0'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_member_with_invalid_fields(self):
        data = {
            'firstName': 'The 14',
            'lastName': 'Member',
            'taxId': '12345678909',
            'email': 'tenthmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        member_id = response_json['id']

        data = {
            'first_name': 'The 41',
        }
        
        url = f'http://127.0.0.1:8000/members/{member_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_member_with_failed_validation(self):
        Members.objects.create(
            firstName='The 1000',
            lastName='Member',
            email='1000member@email.com',
            access='True',
        )

        data = {
            'firstName': 'The 15',
            'lastName': 'Member',
            'taxId': '12345678909',
            'email': '15member@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        member_id = response_json['id']

        data = {
            'email': '1000member@email.com',
        }
        
        url = f'http://127.0.0.1:8000/members/{member_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_member(self):
        data = {
            'firstName': 'The 16',
            'lastName': 'Member',
            'taxId': '12345678309',
            'email': '16member@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        member_id = response_json['id']

        data = {
            'firstName': 'The Sixteenth',
        }
        
        url = f'http://127.0.0.1:8000/members/{member_id}'
        response = self.client.delete(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_member_whithout_registered_business(self):
        fifth_owner = User.objects.create_superuser(
            id='J23O4K2J3R93URP2OI3J23239K',
            name='Fifth Owner',
            username='fifthowner',
            email='fifthowner@email.com',
            password='thefifthownerpassword',
        )
        refresh = RefreshToken.for_user(fifth_owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = f'http://127.0.0.1:8000/members/198'
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_delete_member_with_deactivated_business(self):
        data = {
            'firstName': 'The 2',
            'lastName': 'Member',
            'taxId': '12345678903',
            'email': '342member@email.com',
            'access': 'True',
        }
        self.client.post(self.url, data=data, format='json')

        self.business.active = False
        self.business.save()

        url = f'http://127.0.0.1:8000/members/98'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_business_with_no_registered_members(self):
        url = f'http://127.0.0.1:8000/members/72'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_not_existing_member(self):
        data = {
            'firstName': 'The 17',
            'lastName': 'Member',
            'taxId': '12345628908',
            'email': '17member@email.com',
            'access': 'True',
        }
        self.client.post(self.url, data=data, format='json')
        
        url = f'http://127.0.0.1:8000/members/0'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
