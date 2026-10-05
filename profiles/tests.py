import io
import shutil
import tempfile

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

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


class ProfileAvatarUploadTest(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media_root)
        self.override.enable()
        self.addCleanup(self.override.disable)
        self.addCleanup(shutil.rmtree, self.media_root, ignore_errors=True)

        self.user = User.objects.create_user(
            email='avatar@example.com',
            password='avatarpass123',
            first_name='Avatar',
        )
        self.client = Client()
        self.client.login(email='avatar@example.com', password='avatarpass123')

    def _image(self):
        buffer = io.BytesIO()
        Image.new('RGB', (10, 10), 'blue').save(buffer, 'PNG')
        buffer.seek(0)
        return SimpleUploadedFile('avatar.png', buffer.read(), content_type='image/png')

    def test_upload_avatar_updates_profile(self):
        response = self.client.post(reverse('profiles:update'), {
            'first_name': 'Avatar',
            'email': 'avatar@example.com',
            'avatar': self._image(),
        })
        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.avatar)
