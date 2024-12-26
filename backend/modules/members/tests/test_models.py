from django.test import TestCase

from . import factories


class TestMembersModes(TestCase):
    def test_str_return(self):
        member = factories.MembersFactory(firstName='The', lastName='Member')
        self.assertEqual(member.__str__(), 'The Member')
