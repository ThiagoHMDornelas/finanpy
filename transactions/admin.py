from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'transaction_type', 'account', 'category', 'date', 'user')
    list_filter = ('transaction_type', 'date')
    search_fields = ('description',)
    raw_id_fields = ('user', 'account', 'category')
    date_hierarchy = 'date'