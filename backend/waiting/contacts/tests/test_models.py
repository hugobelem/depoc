from django.test import TestCase

from .factories import ContactFactory


class TestContactsModel(TestCase):
    def test_str_return(self):
        customer = ContactFactory(name='Customer')
        self.assertEqual(customer.__str__(), 'Customer')
