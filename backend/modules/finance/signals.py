from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import BankAccount, Category

@receiver(pre_save, sender=BankAccount)
@receiver(pre_save, sender=Category)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
