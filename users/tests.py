from django.test import TestCase
from django.db import IntegrityError

from .models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
        )

    def test_create_user_with_email(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertTrue(self.user.is_active)

    def test_email_is_username_field(self):
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_email_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                password='another123',
            )

    def test_create_user_without_email_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpass123')

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_not_staff_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin2@example.com',
                password='adminpass123',
                is_staff=False,
            )

    def test_str_returns_email(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_created_at_and_updated_at(self):
        self.assertIsNotNone(self.user.created_at)
        self.assertIsNotNone(self.user.updated_at)

    def test_email_normalized(self):
        user = User.objects.create_user(
            email='Test@EXAMPLE.com',
            password='testpass123',
        )
        self.assertEqual(user.email, 'Test@example.com')

    def test_required_fields(self):
        self.assertEqual(User.REQUIRED_FIELDS, ['first_name'])
