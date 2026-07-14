from django.db import models
from django.conf import settings


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = (
        ('corrente', 'Corrente'),
        ('poupanca', 'Poupança'),
        ('carteira', 'Carteira'),
        ('investimento', 'Investimento'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='usuário',
    )
    name = models.CharField('nome', max_length=100)
    account_type = models.CharField('tipo', max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='corrente')
    balance = models.DecimalField('saldo', max_digits=12, decimal_places=2, default=0)
    institution = models.CharField('instituição', max_length=100, blank=True, null=True)
    color = models.CharField('cor', max_length=7, default='#7c3aed')
    is_active = models.BooleanField('ativo', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'conta'
        verbose_name_plural = 'contas'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
