from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import Product, ProductCategory, ProductCostHistory

@receiver(pre_save, sender=Product)
@receiver(pre_save, sender=ProductCategory)
@receiver(pre_save, sender=ProductCostHistory)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
