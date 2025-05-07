from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from .factories import UserFactory

from modules.accounts.models import Owner
from modules.business.models import Business

from modules.business.views import BusinessEndpoint


class BusinessEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        self.owner = Owner.objects.create(user=self.user)
        business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        self.owner.business = business
        self.owner.save()

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permision_is_owner(self):
        self.owner.delete()
        request = self.factory.get(
            'business',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = BusinessEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_creating_many_business(self):
        data = {}
        request = self.factory.post(
            'business',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = BusinessEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['error']['message'], 'Owner has an existing business.'
        )
