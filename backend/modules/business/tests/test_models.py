from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from modules.business.models import Business, BusinessOwner


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
            email=None,
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


    def test_unique_registration_number(self):
        with self.assertRaises(IntegrityError):
            Business.objects.create(
                legalName='Business3 Inc',
                tradeName='Biz3',
                registrationNumber='01234567891234',
            )             


    def test_unique_ulid(self):
        with self.assertRaises(IntegrityError):
            Business.objects.create(
                id='01JFJT8RTWQBMQJ6CGEE2Q0M77',
                legalName='Business3 Inc',
                tradeName='Biz3',
                registrationNumber='01234567891235',
            )      


    def test_optional_fields(self):
        self.assertIsNone(self.business.email)
        self.assertEqual(self.business.stateRegistration, '')
        self.assertEqual(self.business.cityRegistration, '')
        self.assertEqual(self.business.companyType, '')
        self.assertEqual(self.business.streetAddress, '')
        self.assertEqual(self.business.addressNumber, '')
        self.assertEqual(self.business.neighborhood, '')
        self.assertEqual(self.business.city, '')
        self.assertEqual(self.business.state, '')
        self.assertEqual(self.business.postCode, '')
        self.assertEqual(self.business.category, '')       
    

class BusinessOwnerTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            name='Name',
            username='name',
            email='name@email.com',
            password='namepassword'
        )
        self.business = Business.objects.create(
            id='01JFJT8RTWQBMQJ6CGEE2Q0M77',
            legalName='Business Inc',
            tradeName='Biz',
            registrationNumber='01234567891234'
        )        
        self.busines_owner = BusinessOwner.objects.create(
            owner=self.owner,
            business=self.business
        )
    

    def test_business_owner_creation(self):
        self.assertEqual(self.busines_owner.owner, self.owner)
        self.assertEqual(self.busines_owner.business, self.business)    


    def test_one_to_one_constraints(self):
        self.new_business = Business.objects.create(
            id='01JFJT8RTWQBMQJ6CGEE2Q0M78',
            legalName='Business2 Inc',
            tradeName='Biz2',
            registrationNumber='01234567891235'
        )      
        with self.assertRaises(IntegrityError):
            self.owner_with_business = BusinessOwner.objects.create(
                owner=self.owner,
                business=self.new_business
            )
