from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.transactions'
    label = 'modules_transactions'
    verbose_name = 'Finance Transactions'

    def ready(self):
        from . import signals
