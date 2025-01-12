from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Members, MembersCredentials

import ulid


@receiver(pre_delete, sender=Members)
def delete_member_credentials(sender, instance, **kwargs):
    member = instance
    if hasattr(member, 'member_credentials'):
        try:
            members_credentials = member.member_credentials
            credential = members_credentials.credential
            credential.delete()
        except Exception as e:
            # Exception could be logged
            pass


@receiver(pre_save, sender=Members)
@receiver(pre_save, sender=MembersCredentials)
def generate_ulids(sender, instance, **kwargs):
    if not instance.id:
        instance.id = ulid.new().str
