from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.products'
    module = 'modules'
    label = 'products'

    def ready(self):
        from . import signals
