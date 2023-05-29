from django.test import TestCase
from .models import User
from django.db import IntegrityError

class UserModelTest(TestCase):
    user_data = {'name': 'Test User', 'email': 'test@example.com', 'password': '123456'}
    
    def test_create_superuser(self):
        user = User.objects.create_superuser(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)

    def test_superuser_must_be_superuser(self):
        with self.assertRaises(ValueError) as cm:
            User.objects.create_superuser(**self.user_data, is_superuser=False)
        exception = cm.exception
        self.assertEquals(str(exception), 'Superuser must have is_superuser=True.')

    def test_superuser_must_be_staff(self):
        with self.assertRaises(ValueError) as cm:
            User.objects.create_superuser(**self.user_data, is_staff=False)
        exception = cm.exception
        self.assertEquals(str(exception), 'Superuser must have is_staff=True.')

    def test_superuser_must_be_active(self):
        with self.assertRaises(ValueError) as cm:
            User.objects.create_superuser(**self.user_data, is_active=False)
        exception = cm.exception
        self.assertEquals(str(exception), 'Superuser must have is_active=True.')
    
    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertIsInstance(user, User)

    def test_str_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEquals(str(user), 'Test User')

    def test_password_is_hashed(self):
        user = User.objects.create_user(**self.user_data)
        self.assertNotEquals(user.password, '123456')
        self.assertTrue(user.check_password('123456'))

    def test_email_must_be_unique(self):
        User.objects.create_user(**self.user_data)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)