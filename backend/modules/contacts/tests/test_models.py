from django.test import TestCase

from modules.contacts.models import Contacts


class TestContactsModel(TestCase):
    def setUp(self):
        self.customer = Contacts.objects.create(
         name='Customer',
         code='1',
         entityType='PERSON',
         contactType='CUSTOMER',   
        )
    
    def test_str_return(self):
        self.assertEqual(self.customer.__str__(), 'Customer')
