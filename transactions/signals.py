from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Transaction


@receiver(pre_save, sender=Transaction)
def store_original_transaction(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._original_amount = Transaction.objects.get(pk=instance.pk).amount
            instance._original_type = Transaction.objects.get(pk=instance.pk).transaction_type
            instance._original_account_id = Transaction.objects.get(pk=instance.pk).account_id
        except Transaction.DoesNotExist:
            pass


@receiver(post_save, sender=Transaction)
def update_account_balance_on_save(sender, instance, created, **kwargs):
    account = instance.account
    if created:
        if instance.transaction_type == 'entrada':
            account.balance += instance.amount
        else:
            account.balance -= instance.amount
        account.save()
    else:
        original_amount = getattr(instance, '_original_amount', instance.amount)
        original_type = getattr(instance, '_original_type', instance.transaction_type)
        original_account_id = getattr(instance, '_original_account_id', instance.account_id)

        if original_account_id != instance.account_id:
            from accounts.models import Account
            old_account = Account.objects.get(pk=original_account_id)
            if original_type == 'entrada':
                old_account.balance -= original_amount
            else:
                old_account.balance += original_amount
            old_account.save()

            if instance.transaction_type == 'entrada':
                account.balance += instance.amount
            else:
                account.balance -= instance.amount
            account.save()
        else:
            if original_type == 'entrada':
                account.balance -= original_amount
            else:
                account.balance += original_amount

            if instance.transaction_type == 'entrada':
                account.balance += instance.amount
            else:
                account.balance -= instance.amount
            account.save()


@receiver(post_delete, sender=Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    account = instance.account
    if instance.transaction_type == 'entrada':
        account.balance -= instance.amount
    else:
        account.balance += instance.amount
    account.save()