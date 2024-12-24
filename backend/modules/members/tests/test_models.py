from django.test import TestCase
from django.db.utils import IntegrityError

from modules.members.models import Members, MembersCredentials

import ulid


class MembersTest(TestCase):
    def setUp(self):
        self.member = Members.objects.create(
            id='J23O4K2J3R93URP2OI3J2323KJ',
            firstName="Member",
            lastName="Self",
            taxId="01234567891234",
            dateOfBirth="2024-09-03", 
            role="admin",
            status="active",
            hireDate="2009-08-12",
            position="CEO",
            salary="35",
            streetAddress="Street",
            addressNumber="123",
            neighborhood="Park",
            city="Green Land",
            state="Portela",
            postCode="0923829",
            phone="87757385873",
            email="memberself@email.com",
            access="False",
        )


    def test_member_creation(selft):
        selft.assertEqual(selft.member.id, 'J23O4K2J3R93URP2OI3J2323KJ')

        
    def test_required_fields(self):
        member = Members.objects.create(
            id='J23O4K2J3R93URP2OI3J2323KK',
            # firstName="Member",
            # lastName="Self",
            # email="memberself2@email.com",
        )
        with self.assertRaises(Exception) as context:
            member.full_clean()
        self.assertIn('email', str(context.exception))
        self.assertIn('firstName', str(context.exception))
        self.assertIn('lastName', str(context.exception))

    
    def test_unique_tax_id(self):
        with self.assertRaises(IntegrityError):
            Members.objects.create(
                id='J23O4K2J3R93URP2OI3J2323KL',
                firstName="Member",
                lastName="Self",
                email="memberself3@email.com",
                taxId="01234567891234",
            )

    
    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            Members.objects.create(
                id='J23O4K2J3R93URP2OI3J2323KM',
                firstName="Member",
                lastName="Self",
                email="memberself@email.com",
                taxId="01234567891235",
            )


    def test_unique_ulid(self):
        with self.assertRaises(IntegrityError):
            Members.objects.create(
                id='J23O4K2J3R93URP2OI3J2323KJ',
                firstName="Member",
                lastName="Self",
                email="memberself4@email.com",
                taxId="01234567349230",
            )


    def test_optional_fields(self):
        member = Members.objects.create(
            id='J23O4K2J3R94URP2OI3J2323KJ',
            firstName="Member",
            lastName="Self",
            email="memberself5@email.com",
        )
        member.full_clean()
        self.assertEqual(member.id, 'J23O4K2J3R94URP2OI3J2323KJ')

    
class MembersCredentialsTest(TestCase):
    def setUp(self):
        return super().setUp()
    

    def test_members_credentials_creation(self):
        ...

    
    def test_foreign_key(self):
        ...