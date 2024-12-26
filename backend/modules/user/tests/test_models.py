from django.test import TestCase

from . import factories


class TestUserModel(TestCase):
    def test_str_return(self):
        user = factories.UserFactory(email='user@email.com')
        self.assertEqual(user.__str__(), 'user@email.com')