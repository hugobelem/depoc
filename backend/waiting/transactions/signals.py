from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.db.models import Sum

import ulid

from .models import Transaction

@receiver(pre_save, sender=Transaction)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str


@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_bank_account_balance(sender, instance, **kwargs):
    with transaction.atomic():
        bank_account = instance.bankAccount
        total_debit = Transaction.objects\
            .filter(bankAccount=bank_account)\
            .aggregate(Sum('amount'))['amount__sum'] or 0

        bank_account.balance = total_debit
        bank_account.save()


@receiver(post_save, sender=Transaction)
def link_transactions(sender, instance, created, **kwargs):
    linked_transaction = instance.linkedTransaction
    if created and linked_transaction:
        linked_transaction.linkedTransaction = instance
        linked_transaction.save()
