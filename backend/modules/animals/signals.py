from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import Animals

@receiver(pre_save, sender=Animals)
def generate_ulid(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str