from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Members


@receiver(pre_delete, sender=Members)
def delete_member_credentials(sender, instance, **kwargs):
    member = instance
    if hasattr(member, 'credentials') and member.credentials:
        try:
            members_credentials = member.credentials
            credentials = members_credentials.credentials
            credentials.delete()
        except Exception as e:
            # Exception could be logged
            pass
