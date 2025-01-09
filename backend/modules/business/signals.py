from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import (
    Business,
    BusinessOwner,
    BusinessMembers,
    BusinessContacts,
    BusinessProducts,
    BusinessProductsCategories,
    BusinessBankAccounts,
    BusinessFinanceCategories,
)

@receiver(pre_save, sender=Business)
@receiver(pre_save, sender=BusinessOwner)
@receiver(pre_save, sender=BusinessMembers)
@receiver(pre_save, sender=BusinessContacts)
@receiver(pre_save, sender=BusinessProducts)
@receiver(pre_save, sender=BusinessProductsCategories)
@receiver(pre_save, sender=BusinessBankAccounts)
@receiver(pre_save, sender=BusinessFinanceCategories)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
