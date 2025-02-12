from django.contrib import admin
from django.contrib.admin import register


from .models import Payment


@register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'contact',
        'total_amount',
        'due_at',
        'status',
        'payment_type',
        'business',
    ]

    readonly_fields = ['amount_paid', 'outstanding_balance', 'status']
