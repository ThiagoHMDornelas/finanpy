from django.db import models
from django.conf import settings


class Category(models.Model):
    CATEGORY_TYPE_CHOICES = (
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='usuário',
    )
    name = models.CharField('nome', max_length=100)
    category_type = models.CharField('tipo', max_length=10, choices=CATEGORY_TYPE_CHOICES)
    color = models.CharField('cor', max_length=7, default='#7c3aed')
    icon = models.CharField('ícone', max_length=50, blank=True, null=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['category_type', 'name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name