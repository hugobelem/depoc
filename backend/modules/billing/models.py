from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Payment(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partially_paid', 'Partially Paid'),
    ]

    PAYMENT_TYPE = [
        ('payable', 'Payable'),
        ('receivable', 'Receivable'),
    ]

    RECURRENCE_OPTIONS = [
        ('once', 'Once'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('installments', 'Installments'),
    ]

    WEEKDAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )

    contact = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.PROTECT,
        related_name='payments',
    )

    category = models.ForeignKey(
        'finance.FinancialCategory',
        on_delete=models.DO_NOTHING,
        related_name='payments',
        blank=True,
        null=True,
    )

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='payments',
        blank=True,
        null=True,
    )

    issued_at = models.DateField()
    due_at = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    payment_type = models.CharField(max_length=150, choices=PAYMENT_TYPE)
    status = models.CharField(
        max_length=150,
        choices=PAYMENT_STATUS,
        default='pending',
    )
    paid_at = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=150, blank=True, null=True)
    recurrence = models.CharField(
        max_length=150,
        choices=RECURRENCE_OPTIONS,
        default='once',
    )
    installment_count = models.PositiveIntegerField(blank=True, null=True)
    due_weekday = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        choices=WEEKDAYS,
    )
    due_day_of_month = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
    )
    reference = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    notes = models.TextField(max_length=500, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        if self.recurrence == 'installments':
            if not self.installments:
                raise ValidationError(
                    {
                        'installments': 
                        'This field is required if recurrence is "installments".'                    
                    }
                )
            elif not self.due_day:
                raise ValidationError(
                    {
                        'due_day': 
                        'This field is required if recurrence is "installments".',
                    }
                )
        elif self.recurrence == 'weekly' and not self.due_weekday:
                raise ValidationError(
                    {
                        'due_weekday': 
                        'This field is required if recurrence is "weekly".'                    
                    }
                )


    def __str__(self):
        return f'ID: {self.id}'
