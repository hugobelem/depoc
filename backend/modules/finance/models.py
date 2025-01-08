from django.db import models


class BankAccount(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )
    bankName = models.CharField(max_length=255)
    branchCode = models.CharField(max_length=255, blank=True)
    accountNumber = models.CharField(max_length=255, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='ACTIVE')

    def __str__(self):
        return self.bankName