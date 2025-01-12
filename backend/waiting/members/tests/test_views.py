from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from modules.members.throttling import BurstRateThrottle
from modules.members.models import Members, MembersCredentials

from django.contrib.auth import get_user_model

User = get_user_model()

from . import factories


class TestMembersEndpointView(APITestCase):
    def setUp(self):
        BurstRateThrottle.rate = '100/min'

        self.owner = factories.OwnerFactory()
        self.business = factories.BusinessFactory()
        self.business_owner = factories.BusinessOwnerFactory(
            owner=self.owner,
            business=self.business
        )

        refresh = RefreshToken.for_user(self.owner)
        self.url = 'http://127.0.0.1:8000/members'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_permission(self):
        member = factories.UserFactory()

        refresh = RefreshToken.for_user(member)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_post_member(self):
        data = {
            'firstName': 'The',
            'lastName': 'Member',
            'taxId': '12345678901',
            'email': 'member@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_member_generate_credentials(self):
        '''
        Send POST request to test if the credentials are generated
        using the member's first name, last name, and email when the member
        is created with the "access" attribute set to True.
        '''
        data = {
            'firstName': 'The',
            'lastName': 'Member',
            'taxId': '12345678901',
            'email': 'member@email.com',
            'access': 'True',
        }
        
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the member created
        response_json = response.json()
        member_id = response_json['id']
        member = Members.objects.get(id=member_id)

        # Get the member's credential
        credential = member.member_credentials.credential

        # Check member and credential matching fields
        self.assertEqual(credential.name, 'The Member')
        self.assertEqual(credential.email, 'member@email.com')


    def test_post_member_whithout_associated_business(self):
        '''
        Send POST request to test member creation when
        the Owner is not associated with a business.
        '''
        owner = factories.OwnerFactory()

        refresh = RefreshToken.for_user(owner)
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


    def test_post_member_with_deactivated_business(self):
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


    def test_post_member_with_no_data(self):
        data = {}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_member_with_invalid_fields(self):
        data = {
            'first_name': 'The Fourth',
            'lastName': 'Member',
            'taxId': '12345678904',
            'email': 'fourthmember@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_member_with_failed_validation(self):
        '''
        Send a POST request to create a member with an email
        that is already associated with a registered member.
        '''
        factories.MembersFactory(email='user@email.com')

        data = {
            'firstName': 'The',
            'lastName': 'User',
            'taxId': '12345678905',
            'email': 'user@email.com',
        }
        
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_members(self):
        factories.Members(firstName='The One')
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


    def test_get_members_whithout_associated_business(self):
        '''
        Send GET request to test member retrieval when
        the Owner is not associated with a business.
        '''
        owner = factories.OwnerFactory()
        
        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_members_with_deactivated_business(self):
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


    def test_get_one_member(self):
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


    def test_get_members_when_business_has_no_members(self):
        '''
        This test sends a GET request to retrieve the members of a business
        that has no registered members.
        '''
        url = f'http://127.0.0.1:8000/members/23432'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_non_existing_member(self):
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
    

    def test_patch_member(self):
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


    def test_patch_member_whithout_associated_business(self):
        owner = factories.OwnerFactory()

        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        data = {
            'firstName': 'The Unkown',
        }
        
        url = f'http://127.0.0.1:8000/members/12'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_patch_member_with_deactivated_business(self):
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


    def test_patch_member_without_registered_members(self):
        data = {
            'firstName': 'The 72',
        }
        url = f'http://127.0.0.1:8000/members/72'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_member_with_no_data(self):
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


    def test_patch_non_existing_member(self):
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


    def test_patch_member_with_invalid_fields(self):
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


    def test_patch_member_with_failed_validation(self):
        factories.MembersFactory(email='1000member@email.com')

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
        owner = factories.OwnerFactory()
        
        refresh = RefreshToken.for_user(owner)
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


    def test_delete_member_without_registered_members(self):
        url = f'http://127.0.0.1:8000/members/72'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_non_existing_member(self):
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


    def test_delete_credential_on_member_deletion(self):
        data = {
            'firstName': 'The',
            'lastName': 'Member',
            'taxId': '12345678901',
            'email': 'member@email.com',
            'access': 'True',
        }
        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        member_id = response_json['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Members.objects.get(id=member_id)
        self.assertTrue(member.member_credentials)

        member.delete()
        member.save()

        with self.assertRaises(MembersCredentials.DoesNotExist):
            MembersCredentials.objects.get(member=member)

        credentials_id = member.member_credentials.credential.id
        with self.assertRaises(User.DoesNotExist):        
            User.objects.get(id=credentials_id)
