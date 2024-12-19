from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.db.utils import IntegrityError

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            id="1",
            name="Name",
            email="name@email.com",
            username="name",        
            password="password",    
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "name@email.com")
        self.assertEqual(self.user.name, "Name")
        self.assertEqual(self.user.username, "name")
        self.assertEqual(str(self.user), "name@email.com")

    def test_required_name(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="2",
                name=None,
                email="name2@email.com",
                username="name2",
            )

    def test_required_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="3",
                name="Name3",
                email=None,
                username="name3",
            )       

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="4",
                name="Name4",
                email="name@email.com",
                username="name4",     
            )

    def test_optional_username(self):
        user_without_username = User.objects.create(
            id="5",
            name="Name5",
            email="name5@email.com",
            username=None,
        )
        self.assertIsNone(user_without_username.username)

    def test_unique_username(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                id="6",
                name="Name6",
                email="name6@email.com",
                username="name",     
            )

    def test_authenticate_with_email(self):
        '''
        This test validates the functionality of the EmailOrUsernameBackend 
        defined in `backends.py`. It ensures that users can successfully
        authenticate using their email address as a username alternative.
        '''
        user = authenticate(username='name@email.com', password='password')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)  

