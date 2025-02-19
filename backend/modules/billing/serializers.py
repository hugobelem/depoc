from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['outstanding_balance']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'payment': {
                'id': instance.id,
                'contact': str(instance.contact),
                'category': str(instance.category),
                'issued_at': representation.pop('issued_at'),
                'due_at': representation.pop('due_at'),
                'paid_at': representation.pop('paid_at'),   
                'updated_at': representation.pop('updated_at'),
                'total_amount': representation.pop('total_amount'),
                'amount_paid': representation.pop('amount_paid'),
                'outstanding_balance': representation.pop('outstanding_balance'),
                'payment_type': representation.pop('payment_type'),
                'payment_method': representation.pop('payment_method'),
                'status': representation.pop('status'),
                'recurrence': representation.pop('recurrence'),
                'installment_count': representation.pop('installment_count'),
                'due_weekday': representation.pop('due_weekday'),
                'due_day_of_month': representation.pop('due_day_of_month'),
                'reference': representation.pop('reference'),
                'notes': representation.pop('notes'),
            }
        }
