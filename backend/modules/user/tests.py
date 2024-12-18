from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id="01H5ZZK61PW08F9FB3T3A6PR1",
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
                id="01H5ZZK61PW08F9FB3T3A6PR2",
                name=None,
                email="john.do@example.com",
                username="johndo",
            )

    def test_required_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="01H5ZZK61PW08F9FB3T3A6PR2",
                name="John Doe",
                email=None,
                username="jhdo",
            )       

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="01H5ZZK61PW08F9FB3T3A6PR6",
                name="John Doe",
                email="john.doe@example.com",
                username="jamesdoe",     
            )

    def test_optional_username(self):
        user_without_username = User.objects.create(
            id="01H5ZZK61PW08F9FB3T3A6PR5",
            name="John Doe",
            email="john@example.com",
            username=None,
        )
        self.assertIsNone(user_without_username.username)

    def test_unique_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="01H5ZZK61PW08F9FB3T3A6PR6",
                name="John Doe",
                email="jxdoe@example.com",
                username="johndoe",     
            )

