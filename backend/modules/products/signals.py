from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import Products, Category, CostHistory

@receiver(pre_save, sender=Products)
@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=CostHistory)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
