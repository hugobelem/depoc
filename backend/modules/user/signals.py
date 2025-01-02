from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import User

@receiver(pre_save, sender=User)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
