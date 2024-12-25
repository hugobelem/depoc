from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from modules.members.models import Members, MembersCredentials

User = get_user_model()


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

    
    def test_unique_tax_id_constraint(self):
        with self.assertRaises(IntegrityError):
            Members.objects.create(
                id='J23O4K2J3R93URP2OI3J2323KL',
                firstName="Member",
                lastName="Self",
                email="memberself3@email.com",
                taxId="01234567891234",
            )

    
    def test_unique_email_constraint(self):
        with self.assertRaises(IntegrityError):
            Members.objects.create(
                id='J23O4K2J3R93URP2OI3J2323KM',
                firstName="Member",
                lastName="Self",
                email="memberself@email.com",
                taxId="01234567891235",
            )


    def test_unique_ulid_constraint(self):
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
            taxId='12345678903',
            email="memberself5@email.com",
        )
        member.full_clean()
        self.assertEqual(member.id, 'J23O4K2J3R94URP2OI3J2323KJ')

    
class MembersCredentialsTest(TestCase):
    def setUp(self):
        self.member = Members.objects.create(
            id='J23O4K2J3R93URP2OI3J2323KJ',
            firstName="Member",
            lastName="Self",
            taxId='11234567890',
            email="memberself@email.com",
        )
        self.member.full_clean()        
        self.credential = User.objects.create(
            id='J23O4K2J3R93URP2OI3J7323KJ',
            name='member',
            username='member',
            email='member@email.com',
            password='member@password'
        )
        self.credential.full_clean()
    

    def test_members_credentials_creation(self):
        members_credentials = MembersCredentials.objects.create(
            member=self.member,
            credential=self.credential
        )
        members_credentials.full_clean()
        self.assertEqual(self.member.id, 'J23O4K2J3R93URP2OI3J2323KJ')
        self.assertEqual(self.credential.id, 'J23O4K2J3R93URP2OI3J7323KJ')
