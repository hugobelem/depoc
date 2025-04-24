from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken

from django.test import TestCase

from .factories import UserFactory

from modules.accounts.models import Owner
from modules.business.models import Business
from modules.products.models import Product
from modules.inventory.models import Inventory

from modules.inventory.views import (
    InventoryEndpoint,
    InventoryTransactionEndpoint,
)


class InventoryEndpointViewTest(TestCase):
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
            'inventory',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = InventoryEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)



class InventoryTransactionEndpointViewTest(TestCase):
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

    def test_permision_is_owner(self):
        self.owner.delete()
        request = self.factory.get(
            'inventory/<product_id>/transactions',
            HTTP_AUTHORIZATION=self.auth_header
        )
        response = InventoryTransactionEndpoint.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_inbound_inventory_transaction(self):
        data = {'type': 'inbound', 'quantity': 3}
        request = self.factory.post(
            'inventory/<product_id>/transactions',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = InventoryTransactionEndpoint.as_view()(
            request,
            product_id=self.product.id,
        )

        inventory_id = self.product.inventory.id
        inventory = Inventory.objects.get(id=inventory_id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(inventory.product.stock, 3)

    def test_outbound_inventory_transaction(self):
        data = {'type': 'outbound', 'quantity': 1}
        request = self.factory.post(
            'inventory/<product_id>/transactions',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = InventoryTransactionEndpoint.as_view()(
            request,
            product_id=self.product.id,
        )

        inventory_id = self.product.inventory.id
        inventory = Inventory.objects.get(id=inventory_id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(inventory.product.stock, -1)

    def test_delete_inventory_transaction(self):
        data = {'type': 'inbound', 'quantity': 3}
        request = self.factory.post(
            'inventory/<product_id>/transactions',
            data=data,
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = InventoryTransactionEndpoint.as_view()(
            request,
            product_id=self.product.id,
        )
        transaction_id = response.data['transaction']['id']

        inventory_id = self.product.inventory.id
        inventory = Inventory.objects.get(id=inventory_id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(inventory.product.stock, 3)

        request = self.factory.delete(
            'inventory/<product_id>/transactions/<transaction_id>',
            HTTP_AUTHORIZATION=self.auth_header,
        )
        response = InventoryTransactionEndpoint.as_view()(
            request,
            product_id=self.product.id,
            transaction_id=transaction_id,
        )

        inventory_id = self.product.inventory.id
        inventory = Inventory.objects.get(id=inventory_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(inventory.product.stock, 0)
