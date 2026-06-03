from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category


DEFAULT_CATEGORIES = [
    {'name': 'Alimentação', 'category_type': 'despesa', 'color': '#ef4444'},
    {'name': 'Transporte', 'category_type': 'despesa', 'color': '#f97316'},
    {'name': 'Moradia', 'category_type': 'despesa', 'color': '#eab308'},
    {'name': 'Lazer', 'category_type': 'despesa', 'color': '#8b5cf6'},
    {'name': 'Saúde', 'category_type': 'despesa', 'color': '#22c55e'},
    {'name': 'Educação', 'category_type': 'despesa', 'color': '#3b82f6'},
    {'name': 'Outros', 'category_type': 'despesa', 'color': '#6b7280'},
    {'name': 'Salário', 'category_type': 'receita', 'color': '#22c55e'},
    {'name': 'Freelance', 'category_type': 'receita', 'color': '#3b82f6'},
    {'name': 'Investimentos', 'category_type': 'receita', 'color': '#8b5cf6'},
    {'name': 'Outros', 'category_type': 'receita', 'color': '#6b7280'},
]


@receiver(post_save, sender='users.User')
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        for cat_data in DEFAULT_CATEGORIES:
            Category.objects.get_or_create(
                user=instance,
                name=cat_data['name'],
                defaults={
                    'category_type': cat_data['category_type'],
                    'color': cat_data['color'],
                },
            )