from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'balance', 'user', 'is_active', 'created_at')
    list_filter = ('account_type', 'is_active')
    search_fields = ('name', 'institution')
    raw_id_fields = ('user',)