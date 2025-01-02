from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.user'
    label = 'modules_user'
    verbose_name = 'Users'

    def ready(self):
        from . import signals