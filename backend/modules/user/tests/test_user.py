from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id="1",
            name="John Doe",
            email="john.doe@example.com",
            username="johndoe",            
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.name, "John Doe")
        self.assertEqual(self.user.username, "johndoe")
        self.assertEqual(str(self.user), "john.doe@example.com")

    def test_required_name(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="2",
                name=None,
                email="john.do@example.com",
                username="johndo",
            )

    def test_required_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="3",
                name="John Doe",
                email=None,
                username="jhdo",
            )       

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="4",
                name="John Doe",
                email="john.doe@example.com",
                username="jamesdoe",     
            )

    def test_optional_username(self):
        user_without_username = User.objects.create(
            id="5",
            name="John Doe",
            email="john@example.com",
            username=None,
        )
        self.assertIsNone(user_without_username.username)

    def test_unique_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="6",
                name="John Doe",
                email="jxdoe@example.com",
                username="johndoe",     
            )

