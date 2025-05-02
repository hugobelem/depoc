from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from .factories import UserFactory

from modules.accounts.models import Owner
from modules.business.models import Business
from modules.finance.models import FinancialAccount

from modules.finance.views import (
    FinancialAccountEndpoint,
    FinancialCategoryEndpoint,
    FinancialTransactionEndpoint,
    FinancialTransactionSearchEndpoint,
)


class FinancialAccountEndpointViewTest(TestCase):
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
            'finance/accounts',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = FinancialAccountEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)


class FinancialCategoryEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()

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


class FinancialTransactionEndpointViewTest(TestCase):
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

        self.account = FinancialAccount.objects.create(
            name='Bank',
            business=business,
        )

        self.account2 = FinancialAccount.objects.create(
            name='New Bank',
            business=business,
        )

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permision_is_admin(self):
        self.user.is_staff = False
        self.user.save()

        request = self.factory.get(
            'finance/transactions',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = FinancialTransactionEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_create_credit_finacial_transaction(self):
        data = {
            'type': 'credit',
            'amount': 90,
            'account': self.account.id,
            'description': 'Credit Transaction Test',
        }
        request = self.factory.post(
            'finance/transactions',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = FinancialTransactionEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)
    
        account = FinancialAccount.objects.get(id=self.account.id)
        self.assertEqual(account.balance, 90.00)

    def test_create_debit_finacial_transaction(self):
        data = {
            'type': 'debit',
            'amount': 10,
            'account': self.account.id,
            'description': 'Debit Transaction Test',
        }
        request = self.factory.post(
            'finance/transactions',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = FinancialTransactionEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)
    
        account = FinancialAccount.objects.get(id=self.account.id)
        self.assertEqual(account.balance, -10.00)

    def test_create_transfer_finacial_transaction(self):
        data = {
            'type': 'transfer',
            'amount': 15,
            'account': self.account.id,
            'send_to': self.account2.id,
            'description': 'Transfer Transaction Test',
        }
        request = self.factory.post(
            'finance/transactions',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = FinancialTransactionEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 201)
    
        account = FinancialAccount.objects.get(id=self.account.id)
        self.assertEqual(account.balance, -15.00)

        account2 = FinancialAccount.objects.get(id=self.account2.id)
        self.assertEqual(account2.balance, 15.00)


class FinancilTransactionSearchEndpointViewTest(TestCase):
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

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'finance/transactions/?search=abc',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = FinancialTransactionSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_invalid_query_params(self):
        request = self.factory.get(
            'finance/transactions/?dats',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = FinancialTransactionSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_length_search_query_param(self):
        request = self.factory.get(
            'finance/transactions/?search=ab',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = FinancialTransactionSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_invalid_date_format(self):
        request = self.factory.get(
            'finance/transactions/?date=2025-03-001',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = FinancialTransactionSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)
