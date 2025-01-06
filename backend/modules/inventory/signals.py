from django.db.models.signals import pre_save, post_delete
from django.db import transaction
from django.db.models import Sum
from django.dispatch import receiver

import ulid

from .models import Inventory, InventoryTransaction


@receiver(pre_save, sender=Inventory)
@receiver(pre_save, sender=InventoryTransaction)
def generate_ulid(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
 

@receiver(pre_save, sender=InventoryTransaction)
def update_inventory_quantity(sender, instance, **kwargs):
    with transaction.atomic():
        inventory = instance.inventory

        total_quantity = InventoryTransaction.objects\
            .filter(inventory=inventory)\
            .aggregate(Sum('quantity'))['quantity__sum'] or 0

        inventory.quantity = total_quantity
        inventory.save()

@receiver(post_delete, sender=InventoryTransaction)
def update_inventory_quantity_on_delete(sender, instance, **kwargs):
    with transaction.atomic():
        inventory = instance.inventory

        total_quantity = InventoryTransaction.objects\
            .filter(inventory=inventory)\
            .aggregate(Sum('quantity'))['quantity__sum'] or 0

        inventory.quantity = total_quantity
        inventory.save()
