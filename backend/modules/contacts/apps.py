from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.contacts'
    module = 'module'
    label = 'contacts'
    
    def ready(self):
        from . import signals
