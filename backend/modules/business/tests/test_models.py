from django.test import TestCase

from . import factories


class TestBusinessModel(TestCase):
    def test_str_return(self):
        business = factories.BusinessFactory(legalName='Biz Inc')
        self.assertEqual(business.__str__(), 'Biz Inc')


class TestBusinessOwnerModel(TestCase):
    def test_str_return(self):
        owner = factories.OwnerFactory(email='owner@email.com')
        business = factories.BusinessFactory(legalName='Owner LTDA')
        business_owner = factories.BusinessOwnerFactory(
            owner=owner,
            business=business
        )
        self.assertEqual(
            business_owner.__str__(), 
            'owner@email.com owns Owner LTDA'
        )

