from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import Customer, Supplier


@receiver(pre_save, sender=Customer)
@receiver(pre_save, sender=Supplier)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
