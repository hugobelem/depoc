from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from modules.contacts.throttling import BurstRateThrottle

from . import factories

User = get_user_model()


class TestContactsEndpointView(APITestCase):
    def setUp(self):
        BurstRateThrottle.rate = '100/min'

        self.owner = factories.OwnerFactory()
        self.business = factories.BusinessFactory()
        self.business_owner = factories.BusinessOwnerFactory(
            owner=self.owner,
            business=self.business
        )

        refresh = RefreshToken.for_user(self.owner)
        self.url = 'http://127.0.0.1:8000/contacts'
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_permission(self):
        contacts = factories.UserFactory()

        refresh = RefreshToken.for_user(contacts)
        self.token = str(refresh.access_token)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_post_contact(self):
        contact = factories.ContactData()
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_contact_with_deactivated_business(self):
        self.business.active = False
        self.business.save()

        contact = factories.ContactData()
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_contact_whithout_associated_business(self):
        owner = factories.OwnerFactory()
        
        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        contact = factories.ContactData()
        data = contact.data()

        response = client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_post_contact_with_no_data(self):
        data = {}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_contact_with_invalid_fields(self):
        contact = factories.ContactData(alais='nickname')
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_contact_with_failed_validation(self):
        factories.ContactFactory(code='1')

        contact = factories.ContactData(code='1')
        data = contact.data()
        
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_contacts(self):
        contact = factories.ContactData(name='Customer')
        data = contact.data()
        self.client.post(self.url, data=data, format='json')

        contact = factories.ContactData(name='Supplier')
        data = contact.data()
        self.client.post(self.url, data=data, format='json')
        
        response = self.client.get(self.url, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json[0]['details']['name'], 'Customer')
        self.assertEqual(response_json[1]['details']['name'], 'Supplier')


    def test_get_contacts_whithout_associated_business(self):
        owner = factories.OwnerFactory()
        
        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_contacts_with_deactivated_business(self):
        contact = factories.ContactData(name='Contact')
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response_json['details']['name'], 'Contact')

        self.business.active = False
        self.business.save()

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_one_contact(self):
        contact = factories.ContactData(name='The One')
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        contact_id = response_json['id']
        
        url = f'http://127.0.0.1:8000/contacts/{contact_id}'
        response = self.client.get(url, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['details']['name'], 'The One')


    def test_get_contact_when_business_has_no_contacts(self):
        url = f'http://127.0.0.1:8000/contacts/23432'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_non_existing_contacts(self):
        contact = factories.ContactData()
        data = contact.data()
        
        url = f'http://127.0.0.1:8000/contacts/0'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

    def test_patch_contact(self):
        contact = factories.ContactData()
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        contact_id = response_json['id']

        data = {
            'name': 'The Contact',
        }
        
        url = f'http://127.0.0.1:8000/contacts/{contact_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['details']['name'], 'The Contact')


    def test_patch_contact_whithout_associated_business(self):
        owner = factories.OwnerFactory()
        
        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        data = {
            'name': 'The Unkown',
        }
        
        url = f'http://127.0.0.1:8000/contacts/12'
        response = client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_patch_contact_with_deactivated_business(self):
        contact = factories.ContactData()
        data = contact.data()
        self.client.post(self.url, data=data, format='json')

        self.business.active = False
        self.business.save()

        data = {
            'name': 'The Main Contact',
        }

        url = f'http://127.0.0.1:8000/contacts/98'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_contact_without_registered_contacts(self):
        data = {
            'name': 'The 1',
        }
        url = f'http://127.0.0.1:8000/contacts/72'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_contact_with_no_data(self):
        contact = factories.ContactData()
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        contact_id = response_json['id']

        data = {}
        
        url = f'http://127.0.0.1:8000/contacts/{contact_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_non_existing_contact(self):
        contact = factories.ContactData()
        data = contact.data()
        self.client.post(self.url, data=data, format='json')
        
        data = {'name': 'The 1203',}
        
        url = f'http://127.0.0.1:8000/contacts/0'
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_patch_contact_with_invalid_fields(self):
        contact = factories.ContactData()
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        contact_id = response_json['id']

        data = {
            'nome': 'The Big One',
        }
        
        url = f'http://127.0.0.1:8000/contacts/{contact_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_patch_contact_with_failed_validation(self):
        factories.ContactFactory(code='07')

        contact = factories.ContactData()
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        contact_id = response_json['id']

        data = {
            'code': '07',
        }
        
        url = f'http://127.0.0.1:8000/contacts/{contact_id}'
        response = self.client.patch(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_contact(self):
        contact = factories.ContactData()
        data = contact.data()

        response = self.client.post(self.url, data=data, format='json')
        response_json = response.json()
        contact_id = response_json['id']

        data = {
            'name': 'Customer',
        }
        
        url = f'http://127.0.0.1:8000/contacts/{contact_id}'
        response = self.client.delete(url, data=data, format='json')
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_contact_whithout_associated_business(self):
        owner = factories.OwnerFactory()
        
        refresh = RefreshToken.for_user(owner)
        token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url = f'http://127.0.0.1:8000/contacts/198'
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_delete_contact_with_deactivated_business(self):
        contact = factories.ContactData()
        data = contact.data()

        self.client.post(self.url, data=data, format='json')

        self.business.active = False
        self.business.save()

        url = f'http://127.0.0.1:8000/contacts/98'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_contact_without_registered_contacts(self):
        url = f'http://127.0.0.1:8000/contacts/72'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_non_existing_contact(self):
        contact = factories.ContactData()
        data = contact.data()

        self.client.post(self.url, data=data, format='json')
        
        url = f'http://127.0.0.1:8000/contacts/0'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

