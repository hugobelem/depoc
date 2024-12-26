from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.contacts'
    label = 'modules_contacts'
    verbose_name = 'Contacts'
