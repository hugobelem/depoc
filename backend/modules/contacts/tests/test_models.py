from django.test import TestCase

from .factories import CustomerFactory


class TestContactsModel(TestCase):
    def test_str_return(self):
        customer = CustomerFactory(name='Customer')
        self.assertEqual(customer.__str__(), 'Customer')
