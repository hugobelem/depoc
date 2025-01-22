from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.inventory'
    module = 'modules'
    label = 'inventory'

    def ready(self):
        from . import signals
