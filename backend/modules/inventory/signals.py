from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import Inventory


@receiver(pre_save, sender=Inventory)
def generate_ulid(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
