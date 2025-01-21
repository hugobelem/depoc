from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

import ulid

from .models import Member


@receiver(pre_save, sender=Member)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str


@receiver(post_delete, sender=Member)
def delete_member_credentials(sender, instance, **kwargs):
    member = instance
    credential = member.credential
    if credential:
        credential.delete()
