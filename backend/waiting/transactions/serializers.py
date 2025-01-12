from rest_framework import serializers

from .models import Transaction
from . import services


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
            field for field in fields if field not in (
                'timestamp',
                'createdBy',
                'linkedTransaction',
            )
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
                'category': representation.pop('category'),
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


    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)

        business = self.context['business']
        data = self.context['data']
        request = self.context['request']

        if transaction.type == 'transfer':
            services.complete_transfer(business, data, request, transaction)

        return transaction
