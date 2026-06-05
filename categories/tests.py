from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from .models import Category
from .signals import DEFAULT_CATEGORIES


class CategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
        )

    def test_create_category_custom(self):
        cat = Category.objects.create(
            user=self.user,
            name='Custom Cat',
            category_type='despesa',
            color='#ef4444',
        )
        self.assertEqual(cat.name, 'Custom Cat')
        self.assertEqual(cat.category_type, 'despesa')

    def test_str_returns_name(self):
        cat = Category.objects.get(
            user=self.user,
            name='Alimentação',
        )
        self.assertEqual(str(cat), 'Alimentação')

    def test_created_at_and_updated_at(self):
        cat = Category.objects.filter(user=self.user).first()
        self.assertIsNotNone(cat.created_at)
        self.assertIsNotNone(cat.updated_at)

    def test_default_color(self):
        cat = Category.objects.create(
            user=self.user,
            name='No Color Cat',
            category_type='despesa',
        )
        self.assertEqual(cat.color, '#7c3aed')

    def test_icon_optional(self):
        cat = Category.objects.filter(user=self.user).first()
        self.assertIsNone(cat.icon)

    def test_filter_by_user(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpass123',
            first_name='Other',
        )
        user_cats = Category.objects.filter(user=self.user)
        other_cats = Category.objects.filter(user=other_user)
        self.assertEqual(user_cats.count(), other_cats.count())

    def test_unique_together_user_name(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                user=self.user,
                name='Alimentação',
                category_type='receita',
            )

    def test_cascade_delete_user(self):
        temp_user = User.objects.create_user(
            email='temp@example.com',
            password='temppass123',
            first_name='Temp',
        )
        temp_user_id = temp_user.pk
        Category.objects.create(user=temp_user, name='Temp Cat', category_type='despesa')
        temp_user.delete()
        self.assertEqual(Category.objects.filter(user_id=temp_user_id).count(), 0)


class DefaultCategoriesSignalTest(TestCase):
    def test_default_categories_created_on_user_creation(self):
        user = User.objects.create_user(
            email='new@example.com',
            password='newpass123',
            first_name='New',
        )
        categories = Category.objects.filter(user=user)
        expected = len(DEFAULT_CATEGORIES) - 1
        self.assertEqual(categories.count(), expected)

    def test_default_categories_not_duplicated_on_save(self):
        user = User.objects.create_user(
            email='save@example.com',
            password='savepass123',
            first_name='Save',
        )
        user.first_name = 'Updated'
        user.save()
        expected = len(DEFAULT_CATEGORIES) - 1
        self.assertEqual(Category.objects.filter(user=user).count(), expected)

    def test_default_categories_content(self):
        user = User.objects.create_user(
            email='content@example.com',
            password='contentpass123',
            first_name='Content',
        )
        despesa_count = Category.objects.filter(user=user, category_type='despesa').count()
        receita_count = Category.objects.filter(user=user, category_type='receita').count()
        self.assertEqual(despesa_count, 7)
        self.assertEqual(receita_count, 3)