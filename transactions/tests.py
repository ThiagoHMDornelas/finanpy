from datetime import date
from decimal import Decimal

from django.test import TestCase

from users.models import User
from accounts.models import Account
from categories.models import Category
from .models import Transaction


class TransactionModelTest(TestCase):
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
        )
        self.category = Category.objects.filter(
            user=self.user, category_type='despesa'
        ).first()

    def test_create_transaction(self):
        txn = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            description='Supermercado',
            amount=Decimal('150.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.assertEqual(txn.description, 'Supermercado')
        self.assertEqual(txn.amount, Decimal('150.00'))
        self.assertEqual(txn.transaction_type, 'saida')

    def test_str_returns_description_and_amount(self):
        txn = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            description='Salário',
            amount=Decimal('5000.00'),
            transaction_type='entrada',
            date=date.today(),
        )
        self.assertIn('Salário', str(txn))
        self.assertIn('5000', str(txn))

    def test_created_at_and_updated_at(self):
        txn = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category,
            description='Test',
            amount=Decimal('10.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.assertIsNotNone(txn.created_at)
        self.assertIsNotNone(txn.updated_at)


class TransactionSignalTest(TestCase):
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
        )
        self.category_despesa = Category.objects.filter(
            user=self.user, category_type='despesa'
        ).first()
        self.category_receita = Category.objects.filter(
            user=self.user, category_type='receita'
        ).first()

    def test_saida_decreases_balance(self):
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_despesa,
            description='Mercado',
            amount=Decimal('100.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('900.00'))

    def test_entrada_increases_balance(self):
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_receita,
            description='Salário',
            amount=Decimal('500.00'),
            transaction_type='entrada',
            date=date.today(),
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1500.00'))

    def test_delete_saida_restores_balance(self):
        txn = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_despesa,
            description='Mercado',
            amount=Decimal('100.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('900.00'))

        txn.delete()
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1000.00'))

    def test_delete_entrada_restores_balance(self):
        txn = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_receita,
            description='Salário',
            amount=Decimal('500.00'),
            transaction_type='entrada',
            date=date.today(),
        )
        txn.delete()
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1000.00'))

    def test_update_saida_amount_adjusts_balance(self):
        txn = Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_despesa,
            description='Mercado',
            amount=Decimal('100.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('900.00'))

        txn.amount = Decimal('200.00')
        txn.save()
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('800.00'))

    def test_update_changes_type_adjusts_balance(self):
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

        txn.transaction_type = 'entrada'
        txn.category = self.category_receita
        txn.save()
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1100.00'))

    def test_multiple_transactions(self):
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_receita,
            description='Salário',
            amount=Decimal('5000.00'),
            transaction_type='entrada',
            date=date.today(),
        )
        Transaction.objects.create(
            user=self.user,
            account=self.account,
            category=self.category_despesa,
            description='Aluguel',
            amount=Decimal('1500.00'),
            transaction_type='saida',
            date=date.today(),
        )
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('4500.00'))
