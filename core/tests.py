from datetime import date
from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse

from users.models import User
from accounts.models import Account
from categories.models import Category


PROTECTED_URLS = [
    ('dashboard', {}),
    ('accounts:list', {}),
    ('accounts:create', {}),
    ('categories:list', {}),
    ('categories:create', {}),
    ('transactions:list', {}),
    ('transactions:create', {}),
    ('profiles:detail', {}),
    ('profiles:update', {}),
    ('profiles:password_change', {}),
]


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_register_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_register_valid_data(self):
        response = self.client.post(self.url, {
            'email': 'new@example.com',
            'first_name': 'New',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(self.url, {
            'email': 'new@example.com',
            'first_name': 'New',
            'password1': 'StrongPass123!',
            'password2': 'DifferentPass!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='new@example.com').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user(
            email='existing@example.com',
            password='existingpass123',
            first_name='Existing',
        )
        response = self.client.post(self.url, {
            'email': 'existing@example.com',
            'first_name': 'New',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)

    def test_register_creates_profile(self):
        self.client.post(self.url, {
            'email': 'profile@example.com',
            'first_name': 'Profile',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        user = User.objects.get(email='profile@example.com')
        self.assertTrue(hasattr(user, 'profile'))

    def test_register_creates_default_categories(self):
        self.client.post(self.url, {
            'email': 'cats@example.com',
            'first_name': 'Cats',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        user = User.objects.get(email='cats@example.com')
        self.assertEqual(Category.objects.filter(user=user).count(), 10)

    def test_authenticated_user_redirected_from_register(self):
        user = User.objects.create_user(
            email='auth@example.com',
            password='authpass123',
            first_name='Auth',
        )
        self.client.login(email='auth@example.com', password='authpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class LoginLogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='login@example.com',
            password='loginpass123',
            first_name='Login',
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'login@example.com',
            'password': 'loginpass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'login@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(email='login@example.com', password='loginpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class AccountCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='account@example.com',
            password='accountpass123',
            first_name='Account',
        )
        self.client.login(email='account@example.com', password='accountpass123')

    def test_account_list(self):
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 200)

    def test_account_create(self):
        response = self.client.post(reverse('accounts:create'), {
            'name': 'Nubank',
            'account_type': 'corrente',
            'balance': '1000.00',
            'color': '#7c3aed',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Account.objects.filter(user=self.user, name='Nubank').exists())

    def test_account_update(self):
        account = Account.objects.create(
            user=self.user,
            name='Nubank',
            account_type='corrente',
            balance=Decimal('1000.00'),
        )
        response = self.client.post(
            reverse('accounts:update', kwargs={'pk': account.pk}),
            {
                'name': 'Nubank Atualizado',
                'account_type': 'poupanca',
                'balance': '2000.00',
                'color': '#7c3aed',
            },
        )
        self.assertEqual(response.status_code, 302)
        account.refresh_from_db()
        self.assertEqual(account.name, 'Nubank Atualizado')

    def test_account_delete(self):
        account = Account.objects.create(
            user=self.user,
            name='Nubank',
            account_type='corrente',
            balance=Decimal('1000.00'),
        )
        response = self.client.post(
            reverse('accounts:delete', kwargs={'pk': account.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Account.objects.filter(pk=account.pk).exists())

    def test_account_user_isolation(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpass123',
            first_name='Other',
        )
        Account.objects.create(user=other_user, name='Private Account')
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['accounts']), 0)


class CategoryCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='cat@example.com',
            password='catpass123',
            first_name='Cat',
        )
        self.client.login(email='cat@example.com', password='catpass123')

    def test_category_list(self):
        response = self.client.get(reverse('categories:list'))
        self.assertEqual(response.status_code, 200)

    def test_category_create(self):
        response = self.client.post(reverse('categories:create'), {
            'name': 'Nova Cat',
            'category_type': 'despesa',
            'color': '#ef4444',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(user=self.user, name='Nova Cat').exists())

    def test_category_update(self):
        cat = Category.objects.filter(user=self.user).first()
        response = self.client.post(
            reverse('categories:update', kwargs={'pk': cat.pk}),
            {
                'name': 'Updated Cat',
                'category_type': cat.category_type,
                'color': '#8b5cf6',
            },
        )
        self.assertEqual(response.status_code, 302)
        cat.refresh_from_db()
        self.assertEqual(cat.name, 'Updated Cat')

    def test_category_delete(self):
        cat = Category.objects.create(
            user=self.user,
            name='To Delete',
            category_type='despesa',
        )
        response = self.client.post(
            reverse('categories:delete', kwargs={'pk': cat.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(pk=cat.pk).exists())

    def test_category_user_isolation(self):
        other_user = User.objects.create_user(
            email='other2@example.com',
            password='otherpass123',
            first_name='Other2',
        )
        other_cats_count = Category.objects.filter(user=other_user).count()
        response = self.client.get(reverse('categories:list'))
        self.assertEqual(response.status_code, 200)


class TransactionCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='txn@example.com',
            password='txnpass123',
            first_name='Txn',
        )
        self.client.login(email='txn@example.com', password='txnpass123')
        self.account = Account.objects.create(
            user=self.user,
            name='Nubank',
            account_type='corrente',
            balance=Decimal('1000.00'),
        )
        self.category_despesa = Category.objects.filter(
            user=self.user, category_type='despesa'
        ).first()
        self.category_receita = Category.objects.filter(
            user=self.user, category_type='receita'
        ).first()

    def test_transaction_list(self):
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 200)

    def test_transaction_create_saida(self):
        response = self.client.post(reverse('transactions:create'), {
            'description': 'Supermercado',
            'amount': '100.00',
            'transaction_type': 'saida',
            'date': date.today().strftime('%Y-%m-%d'),
            'category': self.category_despesa.pk,
            'account': self.account.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('900.00'))

    def test_transaction_create_entrada(self):
        response = self.client.post(reverse('transactions:create'), {
            'description': 'Salário',
            'amount': '500.00',
            'transaction_type': 'entrada',
            'date': date.today().strftime('%Y-%m-%d'),
            'category': self.category_receita.pk,
            'account': self.account.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1500.00'))

    def test_transaction_delete_restores_balance(self):
        from transactions.models import Transaction
        txn = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_despesa,
            description='Test',
            amount=Decimal('100.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('900.00'))

        response = self.client.post(
            reverse('transactions:delete', kwargs={'pk': txn.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1000.00'))


class RouteProtectionTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_unauthenticated_redirect(self):
        for url_name, kwargs in PROTECTED_URLS:
            response = self.client.get(reverse(url_name, kwargs=kwargs))
            self.assertIn(
                response.status_code, [302, 301],
                f'Expected redirect for {url_name}, got {response.status_code}',
            )

    def test_authenticated_access(self):
        user = User.objects.create_user(
            email='auth@example.com',
            password='authpass123',
            first_name='Auth',
        )
        self.client.login(email='auth@example.com', password='authpass123')
        for url_name, kwargs in PROTECTED_URLS:
            response = self.client.get(reverse(url_name, kwargs=kwargs))
            self.assertEqual(
                response.status_code, 200,
                f'Expected 200 for {url_name}, got {response.status_code}',
            )

    def test_login_page_accessible(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_accessible(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_landing_page_accessible(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)