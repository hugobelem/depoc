from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
        ('transfer', 'Transfer'),
    ]

    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        'modules_finance.Category',
        on_delete=models.DO_NOTHING,
        related_name='transactions',
        blank=True,
        null=True,
    )
    createdBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    bankAccount = models.ForeignKey(
        'modules_finance.BankAccount',
        on_delete=models.PROTECT,
        related_name='transactions',
    )
    contact = models.ForeignKey(
        'modules_contacts.Contacts',
        on_delete=models.CASCADE,
        related_name='transactions',
        blank=True,
        null=True,
    )
    linkedTransaction = models.OneToOneField(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )    

    def __str__(self):
        return self.description
