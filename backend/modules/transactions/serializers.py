from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'description',
            'type',
            'timestamp',
            'category',
            'createdBy',
            'bankAccount',
            'contact',
            'linkedTransaction',
        ]
        expected_fields = [
            field for field in fields if field not in ('timestamp', 'createdBy')
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'transactionDetails': {
                'amount': representation.pop('amount'),
                'description': representation.pop('description'),
                'type': representation.pop('type'),
                'timestamp': representation.pop('timestamp'),
                'categoryId': representation.pop('category'),
            },
            'metadata': {
                'createdBy': representation.pop('createdBy'),
                'linkedTransaction': representation.pop('linkedTransaction'),
            },
            'relationships': {
                'bankAccount': representation.pop('bankAccount'),
                'contact': representation.pop('contact'),
            },
        }
