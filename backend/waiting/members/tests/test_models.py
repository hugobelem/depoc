from django.test import TestCase

from . import factories


class TestMembersModel(TestCase):
    def test_str_return(self):
        member = factories.MembersFactory(firstName='The', lastName='Member')
        self.assertEqual(member.__str__(), 'The Member')


class TestMembersCredentialsModel(TestCase):
    def test_str_return(self):
        member = factories.MembersFactory(firstName='My', lastName='Member')
        credential = factories.CredentialsFactory(email='mymember@email.com')
        member_credentials = factories.MembersCredentialsFactory(
            member=member,
            credential=credential
        )
        self.assertEqual(
            member_credentials.__str__(),
            'My Member - mymember@email.com'
        )

    def test_member_credential_association(self):
        member = factories.MembersFactory()
        credential = factories.CredentialsFactory()
        member_credentials = factories.MembersCredentialsFactory(
            member=member,
            credential=credential
        )
        self.assertTrue(hasattr(member, 'member_credentials'))
        self.assertTrue(hasattr(credential, 'member_credentials'))
        self.assertTrue(member_credentials.member == member)
        self.assertTrue(member_credentials.credential == credential)