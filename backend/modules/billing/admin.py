from django.contrib import admin
from django.contrib.admin import register


from .models import Payment


@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'total_amount',
        'amount_paid',
        'outstanding_balance',
        'status',
        'due_at',
        'payment_type',
        'contact',
        'business',
    ]

    readonly_fields = ['amount_paid', 'outstanding_balance', 'status']
