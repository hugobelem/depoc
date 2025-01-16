from django.db import models


class FinancialAccount(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='financial_accounts',
    )

    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class FinancialCategory(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='financial_categories',
    )
    
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        blank=True, 
        null=True, 
    )

    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return self.name


class FinancialTransaction(models.Model):
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

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='financial_transactions',
    )

    category = models.ForeignKey(
        FinancialCategory,
        on_delete=models.DO_NOTHING,
        related_name='financial_transactions',
        blank=True,
        null=True,
    )

    operator = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='financial_transactions',
    )

    account = models.ForeignKey(
        FinancialAccount,
        on_delete=models.PROTECT,
        related_name='financial_transactions',
    )

    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.CASCADE,
        related_name='financial_transactions',
        blank=True,
        null=True,
    )

    linked = models.OneToOneField(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )    

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
