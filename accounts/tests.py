from decimal import Decimal
from django.test import TestCase

from users.models import User
from .models import Account


class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Nubank',
            account_type='corrente',
            balance=Decimal('1000.00'),
            institution='Nu Pagamentos',
            color='#8b5cf6',
        )

    def test_create_account(self):
        self.assertEqual(self.account.name, 'Nubank')
        self.assertEqual(self.account.account_type, 'corrente')
        self.assertEqual(self.account.balance, Decimal('1000.00'))

    def test_str_returns_name(self):
        self.assertEqual(str(self.account), 'Nubank')

    def test_created_at_and_updated_at(self):
        self.assertIsNotNone(self.account.created_at)
        self.assertIsNotNone(self.account.updated_at)

    def test_default_values(self):
        account = Account.objects.create(
            user=self.user,
            name='Carteira',
        )
        self.assertEqual(account.account_type, 'corrente')
        self.assertEqual(account.balance, Decimal('0'))
        self.assertTrue(account.is_active)
        self.assertEqual(account.color, '#7c3aed')

    def test_filter_by_user(self):
        other_user = User.objects.create_user(
            email='other@example.com',
            password='otherpass123',
            first_name='Other',
        )
        Account.objects.create(user=other_user, name='Itau')

        user_accounts = Account.objects.filter(user=self.user)
        self.assertEqual(user_accounts.count(), 1)
        self.assertEqual(user_accounts.first().name, 'Nubank')

    def test_account_types(self):
        for acct_type in ['corrente', 'poupanca', 'carteira', 'investimento']:
            Account.objects.create(user=self.user, name=f'Acc-{acct_type}', account_type=acct_type)
        self.assertEqual(Account.objects.filter(user=self.user).count(), 5)

    def test_cascade_delete_user(self):
        user = User.objects.create_user(
            email='temp@example.com',
            password='temppass123',
            first_name='Temp',
        )
        Account.objects.create(user=user, name='Temp Account')
        user_id = user.pk
        user.delete()
        self.assertEqual(Account.objects.filter(user_id=user_id).count(), 0)

    def test_institution_optional(self):
        account = Account.objects.create(user=self.user, name='Simple')
        self.assertIsNone(account.institution)

    def test_balance_updates_on_transaction(self):
        from categories.models import Category
        from transactions.models import Transaction
        from datetime import date

        cat = Category.objects.filter(user=self.user, category_type='despesa').first()
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=cat,
            description='Test',
            amount=Decimal('100.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('900.00'))
