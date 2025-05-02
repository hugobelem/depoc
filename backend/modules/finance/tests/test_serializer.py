import json

from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from .factories import UserFactory

from modules.accounts.models import Owner
from modules.business.models import Business
from modules.finance.models import FinancialCategory

from modules.finance.views import (
    FinancialCategoryEndpoint,
)

class FinancialCategoryEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

        self.owner = Owner.objects.create(user=self.user)
        self.business = Business.objects.create(
            legal_name='The Test Business INC',
            trade_name='Test Business',
            cnpj=12345678901234
        )
        self.owner.business = self.business
        self.owner.save()

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permision_is_admin(self):
        self.user.is_staff = False
        self.user.save()

        request = self.factory.get(
            'finance/categories',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = FinancialCategoryEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_category(self):
        parent_category = FinancialCategory.objects.create(
            name='Parent',
            business=self.business,
        )

        data: dict = {'name': 'Child', 'parent': parent_category.id}

        request = self.factory.post(
            'finance/categories',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = FinancialCategoryEndpoint.as_view()(request)
        nested_parent = response.data['category']['parent']['name']
        self.assertEqual(nested_parent, 'Parent')
