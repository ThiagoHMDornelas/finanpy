from django.db import models
from django.conf import settings


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='usuário',
    )
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='conta',
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='categoria',
    )
    description = models.CharField('descrição', max_length=200)
    amount = models.DecimalField('valor', max_digits=12, decimal_places=2)
    transaction_type = models.CharField('tipo', max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateField('data')
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'transação'
        verbose_name_plural = 'transações'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.description} - R$ {self.amount}'