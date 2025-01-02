from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.products'
    label = 'modules_products'
    verbose_name = 'Products'

    def ready(self):
        from . import signals
