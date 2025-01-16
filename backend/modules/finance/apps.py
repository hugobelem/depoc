from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.finance'
    module = 'modules'
    label = 'finance'

    def ready(self):
        from . import signals
