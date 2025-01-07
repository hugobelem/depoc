from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.finance'
    label = 'modules_finance'
    verbose_name = 'Finance'

    def ready(self):
        from . import signals