from django.test import TestCase
from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError

from modules.business.models import Business, BusinessOwner

User = get_user_model()

class BusinessModelTest(TestCase):
    def setUp(self):
        return super().setUp()
    

    def test_business_creation(self):
        ...


    def test_required_fields(self):
        ...


    def test_optional_fields(self):
        ...


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
