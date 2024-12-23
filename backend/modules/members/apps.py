from django.apps import AppConfig


class MembersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.members'
    label = 'modules_members'
    verbose_name = 'Members'

    def ready(self):
        from . import signals
