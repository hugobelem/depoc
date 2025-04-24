from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from modules.contacts.views import (
    ContactsSearchEndpoint,
    ContactsEndpoint,
    CustomerEndpoint, 
    SupplierEndpoint,
)

from .factories import UserFactory


class ContactsSearchEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'contacts/?search=abc',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ContactsSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_invalid_query_params(self):
        request = self.factory.get(
            'contacts/?dats',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ContactsSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_length_search_query_param(self):
        request = self.factory.get(
            'contacts/?search=ab',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ContactsSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)


class ContactsEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'contacts/?search=abc',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ContactsEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)


class CustomerEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'contacts/customers',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = CustomerEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)


class SupplierEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'contacts/suppliers',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = SupplierEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)
