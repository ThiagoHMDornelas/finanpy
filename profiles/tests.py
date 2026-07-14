from django.test import TestCase

from users.models import User
from .models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
        )

    def test_profile_auto_created_on_user_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsNotNone(self.user.profile)

    def test_profile_str(self):
        self.assertEqual(str(self.user.profile), 'Perfil de test@example.com')

    def test_profile_user_one_to_one(self):
        profile = self.user.profile
        self.assertEqual(profile.user, self.user)

    def test_created_at_and_updated_at(self):
        profile = self.user.profile
        self.assertIsNotNone(profile.created_at)
        self.assertIsNotNone(profile.updated_at)

    def test_avatar_optional(self):
        profile = self.user.profile
        self.assertFalse(bool(profile.avatar))

    def test_cascade_delete_user_deletes_profile(self):
        user = User.objects.create_user(
            email='temp@example.com',
            password='temppass123',
            first_name='Temp',
        )
        profile_pk = user.profile.pk
        user.delete()
        self.assertEqual(Profile.objects.filter(pk=profile_pk).count(), 0)
