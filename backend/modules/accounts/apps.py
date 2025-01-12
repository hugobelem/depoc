from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.accounts'
    module = 'modules'
    label = 'accounts'

    def ready(self):
        from . import signals
