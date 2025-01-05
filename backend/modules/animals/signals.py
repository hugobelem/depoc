from django.db.models.signals import pre_save
from django.dispatch import receiver

import ulid

from .models import (
    Animal,
    AnimalFinancial,
    AnimalLifeCycle,
    AnimalGrowth,
    AnimalWeight,
    AnimalMeatQuality,
    AnimalHealth,
)

@receiver(pre_save, sender=Animal)
@receiver(pre_save, sender=AnimalFinancial)
@receiver(pre_save, sender=AnimalLifeCycle)
@receiver(pre_save, sender=AnimalGrowth)
@receiver(pre_save, sender=AnimalWeight)
@receiver(pre_save, sender=AnimalMeatQuality)
@receiver(pre_save, sender=AnimalHealth)
def generate_ulid(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str