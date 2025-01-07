from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import BankAccount

@receiver(pre_save, sender=BankAccount)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
