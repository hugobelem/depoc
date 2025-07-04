from django.apps import AppConfig


class BusinessConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.business'
    module = 'modules'
    label = 'business'

    def ready(self):
        from . import signals