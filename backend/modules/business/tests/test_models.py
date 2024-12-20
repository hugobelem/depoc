from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from modules.business.models import Business, BusinessOwner

import ulid


User = get_user_model()

class BusinessModelTest(TestCase):
    def setUp(self):
        self.business = Business.objects.create(
            id='01JFJT8RTWQBMQJ6CGEE2Q0M77',
            legalName='Business Inc',
            tradeName='Biz',
            registrationNumber='01234567891234',
            stateRegistration='',
            cityRegistration='',
            companyType='',
            streetAddress='',
            addressNumber='',
            neighborhood='',
            city='',
            state='',
            postCode='',
            phone='',
            email='',
            category='',
            active=True
        )
    

    def test_business_creation(self):
        self.assertEqual(self.business.legalName, 'Business Inc')
        self.assertEqual(self.business.tradeName, 'Biz')
        self.assertEqual(self.business.registrationNumber, '01234567891234')


    def test_missing_required_fields(self):
        with self.assertRaises(IntegrityError):
            Business.objects.create(
                legalName='Business2 Inc',
                tradeName='Biz2',
                registrationNumber=None,
            )


    def test_optional_fields(self):
        self.assertEqual(self.business.stateRegistration, '')
        self.assertEqual(self.business.cityRegistration, '')


    def test_unique_registration_number(self):
        ... 


    def test_access_to_inactive_business(self):
        ...         
    

class BusinessOwnerTest(TestCase):
    def setUp(self):
        ...
    

    def test_business_owner_creation(self):
        ...    
    

    def test_one_to_one_constraints(self):
        ...    
