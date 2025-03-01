from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.apps import apps

import ulid

from .models import FinancialAccount, FinancialCategory, FinancialTransaction


Business = apps.get_model('business', 'Business')

@receiver(post_save, sender=Business)
def create_standard_financial_account(sender, instance, created, **kwargs):
    if created:
        FinancialAccount.objects.create(name='Caixa', business=instance)


@receiver(pre_save, sender=FinancialAccount)
@receiver(pre_save, sender=FinancialCategory)
@receiver(pre_save, sender=FinancialTransaction)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str

@receiver(pre_save, sender=FinancialTransaction)
@receiver(post_save, sender=FinancialTransaction)
@receiver(post_delete, sender=FinancialTransaction)
def update_financial_account_balance(sender, instance, **kwargs):
    financial_account = instance.account
    total_amount = FinancialTransaction.objects\
        .filter(account=financial_account)\
        .aggregate(Sum('amount'))['amount__sum'] or 0

    financial_account.balance = total_amount
    financial_account.save()


@receiver(post_save, sender=FinancialTransaction)
def link_transactions(sender, instance, created, **kwargs):
    linked_transaction = instance.linked
    if created and linked_transaction:
        linked_transaction.linked = instance
        linked_transaction.save()
