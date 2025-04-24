from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from modules.accounts.models import Owner
from modules.business.models import Business
from modules.products.models import Product
from modules.inventory.models import Inventory

from modules.products.views import (
    ProductSearchEndpoint,
    ProductEndpoint,
    ProductCategoryEndpoint,
    ProductCostHistoryEndpoint,
)

from .factories import UserFactory


class ProductSearchEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'products/?search=abc',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_invalid_query_params(self):
        request = self.factory.get(
            'products/?dats',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_length_search_query_param(self):
        request = self.factory.get(
            'products/?search=ab',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductSearchEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 400)


class ProductEndpointViewTest(TestCase):
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
        self.product = Product.objects.create(
            name='Test Product',
            business=business,
        )

        Inventory.objects.create(product=self.product)

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'products',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_update_product_stock(self):
        data = {'stock': 2}

        request = self.factory.patch(
            'products/<product_id>',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductEndpoint.as_view()(
            request,
            product_id=self.product.id
        )

        error_message = ('Adjust stock quantity through an inventory transaction.')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error']['message'], error_message)


class ProductCategoryEndpointViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'products/categories',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductCategoryEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)


class ProductCostHistoryEndpointViewTest(TestCase):
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
        self.product = Product.objects.create(
            name='Test Product',
            business=business,
        )

        Inventory.objects.create(product=self.product)

        self.token = AccessToken.for_user(self.user)
        self.auth_header = f'Bearer {self.token}'

    def test_permission_is_admin(self):
        self.user.is_staff = False
        self.user.save()
        request = self.factory.get(
            'products/<str:product_id>/costs',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductCostHistoryEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_automatic_markup_calculation(self):
        data = {
            'effective_date': '2025-04-24',
            'quantity': 1,
            'cost_price': 25.6,
            'retail_price': 35,
        }
        request = self.factory.post(
            'products/<str:product_id>/costs',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductCostHistoryEndpoint.as_view()(
            request,
            product_id=self.product.id,
        )
        markup = response.data['cost']['markup']
        self.assertEqual(markup, '36.72')

    def test_manual_markup_input(self):
        data = {
            'effective_date': '2025-04-24',
            'quantity': 1,
            'cost_price': 25.6,
            'retail_price': 35,
            'markup': 30,
        }
        request = self.factory.post(
            'products/<str:product_id>/costs',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = ProductCostHistoryEndpoint.as_view()(
            request,
            product_id=self.product.id,
        )
        markup = response.data['cost']['markup']
        self.assertEqual(markup, '30.00')

    def test_automatic_average_cost_calculation(self):
        cost_price = 25
        retail_price = 35
        for _ in range(3):
            data = {
                'effective_date': '2025-04-24',
                'quantity': 53,
                'cost_price': cost_price,
                'retail_price': retail_price,
            }
            request = self.factory.post(
                'products/<str:product_id>/costs',
                data=data,
                HTTP_AUTHORIZATION=self.auth_header
            )
            response = ProductCostHistoryEndpoint.as_view()(
                request,
                product_id=self.product.id,
            )

            cost_price += 8
            retail_price += 4

        average_cost = response.data['cost']['average_cost']
        self.assertEqual(average_cost, '33.00')
