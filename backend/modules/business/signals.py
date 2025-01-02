from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import (
    Business,
    BusinessOwner,
    BusinessMembers,
    BusinessContacts,
    BusinessProducts,
)

@receiver(pre_save, sender=Business)
@receiver(pre_save, sender=BusinessOwner)
@receiver(pre_save, sender=BusinessMembers)
@receiver(pre_save, sender=BusinessContacts)
@receiver(pre_save, sender=BusinessProducts)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
