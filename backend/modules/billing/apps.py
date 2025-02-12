from django.apps import AppConfig


class BillingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.billing'
    module = 'modules'
    label = 'billing'

    def ready(self):
        from . import signals
